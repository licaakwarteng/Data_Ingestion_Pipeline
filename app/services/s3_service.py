import boto3
from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_BUCKET_NAME
)

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

#upload the streamed csv files directly into s3 buckets
def upload_fileobj(file_obj, key: str):
    """
    Upload file-like object to S3.
    """
    s3.upload_fileobj(file_obj, AWS_BUCKET_NAME, key)
    return f"s3://{AWS_BUCKET_NAME}/{key}"



