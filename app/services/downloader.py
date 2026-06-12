import requests
import codecs
from psycopg2 import sql

# stream/ download raw csv files from provided url
def stream_file(url: str, chunk_size: int = 1024 * 1024):
    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        ),
        "Accept": "text/csv,application/octet-stream,*/*",
        "Accept-Language": "en-US,en;q=0.9"
    })

    response = session.get(
        url,
        stream=True,
        timeout=60,
        allow_redirects=True
    )

    response.raise_for_status()

    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            yield chunk



def load_file(conn, s3_client, bucket, key, table):

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    stream = obj["Body"]

    decoder = codecs.getincrementaldecoder("utf-8-sig")()

    copy_sql = sql.SQL("""
        COPY {} FROM STDIN WITH (FORMAT csv, HEADER true)
    """).format(sql.Identifier(table))

    with conn.cursor() as cur:
        try:
            cur.copy_expert(
                copy_sql.as_string(conn),
                stream
            )
        except Exception as e:
            raise RuntimeError(f"COPY failed for {table}: {e}")