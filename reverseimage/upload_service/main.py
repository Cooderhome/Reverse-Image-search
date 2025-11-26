from fastapi import FastAPI, UploadFile, File
from utils.minio_client import upload_image
import redis
import uuid
import io  # Import io

app = FastAPI()

r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}_{file.filename}"
    file_bytes = await file.read()

    # Upload to MinIO
    url = upload_image("images", file_data=io.BytesIO(file_bytes), file_name=file_name, content_type=file.content_type)

    # Publish metadata to Redis
    r.publish("image_uploads", file_name)

    return {"message": "Image uploaded successfully", "file_name": file_name, "url": url}
