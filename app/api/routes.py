from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse
from io import BytesIO
from datetime import datetime
from fastapi import HTTPException
from app.services.downloader import stream_file
from app.services.s3_service import upload_fileobj
from app.services.etl_pipeline import run_pipeline

# creating a router object
router = APIRouter()


# creating new jobs into our database
@router.post("/jobs", response_model=JobResponse)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(
        source_url=str(payload.source_url),
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


# retrieve all jobs in the database
@router.get("/jobs", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.id.desc()).all()
    return jobs


# creating new jobs for our cloud storage from our database
@router.post("/jobs/{job_id}/run")
def run_job(job_id: int, db: Session = Depends(get_db)):

    # select job by id
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    try:
        job.status = "running"
        db.commit()

        # splitting the url into parts and retrieve the name of the file
        parts = job.source_url.split("/")
        name = parts[-1]
        
        if name:
            filename = name
        else:
            filename = f"job_{job.id}.csv"


        # creating a folder name for the job to be stored in s3
        s3_key = f"raw/{datetime.now().date()}/{filename}"

        buffer = BytesIO()
        total_bytes = 0

        for chunk in stream_file(job.source_url):
            buffer.write(chunk)
            total_bytes += len(chunk)

        buffer.seek(0)

        # upload the file object created
        s3_uri = upload_fileobj(buffer, s3_key)

        job.status = "completed"
        job.bytes_processed = total_bytes
        job.s3_key = s3_uri
        job.completed_at = datetime.now()

        db.commit()

        return {
            "message": "Uploaded to S3 successfully",
            "job_id": job.id,
            "s3_key": s3_key,
            "bytes_processed": total_bytes
        }

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        db.commit()

        raise HTTPException(status_code=500, detail=str(e))
    

#for populating tables in neon postgresql database with data from s3
@router.post("/run-etl")
def trigger_etl():
    run_pipeline()
    return {"status": "ETL completed"}

    
