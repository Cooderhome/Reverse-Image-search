from minio import Minio
from minio.error import S3Error

minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

def upload_image(bucket_name, file_data, file_name, content_type):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    minio_client.put_object(
        bucket_name,
        file_name,
        file_data,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=content_type
    )
    return f"http://minio:9000/{bucket_name}/{file_name}"
