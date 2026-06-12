from fastapi import FastAPI
from app.api.routes import router
from app.database import Base, engine
from app.models.job import Job

app = FastAPI(title="Data Ingestion Pipeline")

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Ingestion Pipeline Running"}


