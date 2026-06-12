import boto3
import psycopg2
from psycopg2 import sql
from app.config import (DATABASE_URL, AWS_BUCKET_NAME)
from app.services.registry import FILES_TO_IMPORT
from app.services.downloader import load_file


def s3_stream_chunks(s3_body, chunk_size=1024 * 1024):
    """
    Reliable S3 streaming generator
    """
    return iter(lambda: s3_body.read(chunk_size), b"")


def preview_csv(chunk):
    try:
        text = chunk.decode("utf-8", errors="ignore")
        return text[:300]
    except Exception:
        return "UNREADABLE CHUNK"
    



# stream the csv data from s3 into neon postgresql
def stream_csv_to_postgres(
    conn,
    s3_client,
    bucket_name,
    s3_key,
    table_name,
    chunk_size=1024 * 1024
):

    print(f"Starting import: {s3_key} -> {table_name}")

    # Get S3 object stream
    s3_object = s3_client.get_object(
        Bucket=bucket_name,
        Key=s3_key
    )
    csv_stream = s3_object["Body"]

    copy_sql = sql.SQL("""
    COPY {} FROM STDIN WITH (FORMAT csv, HEADER true)
    """).format(sql.Identifier(table_name))

    with conn.cursor() as cur:
        try:
            cur.copy_expert(copy_sql.as_string(conn), csv_stream)
        except Exception as e:
            print("❌ COPY FAILED:", e)
            conn.rollback()
            raise
 
    print(f"Completed import: {table_name}")


def verify_table(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("SELECT COUNT(*) FROM {}").format(
                sql.Identifier(table_name)
            )
        )
        count = cur.fetchone()[0]
        print(f"{table_name} row count: {count}")
        return count



#create ETL pipeline to repeat process till all csv files are imported to neon postgresql
def run_pipeline():
    s3 = boto3.client("s3")

    with psycopg2.connect(
        DATABASE_URL,
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=10,
        keepalives_count=5
    ) as conn:

        for file in FILES_TO_IMPORT:

            try:

                load_file(
                    conn=conn,
                    s3_client=s3,
                    bucket_name=AWS_BUCKET_NAME,
                    s3_key=file["s3_key"],
                    table_name=file["table"]
                )

                conn.commit()
                verify_table(conn, file["table"])

            except Exception as e:
                conn.rollback()

                print(
                    f"Failed importing "
                    f"{file['s3_key']} "
                    f"-> {file['table']}"
                )

                print(f"Failed: {file['s3_key']} → {file['table']}")
                print("Error:", str(e))


