from minio import Minio
import os

minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

def download_image(bucket_name, file_name, download_path="/tmp"):
    path = os.path.join(download_path, file_name)
    minio_client.fget_object(bucket_name, file_name, path)
    return path
