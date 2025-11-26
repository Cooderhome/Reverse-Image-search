from fastapi import FastAPI, File, UploadFile
from utils.feature_extractor import extract_features_from_bytes
from utils.es_client import search_similar_vectors

app = FastAPI()

@app.post("/search")
async def search_similar(file: UploadFile = File(...)):
    img_bytes = await file.read()
    features = extract_features_from_bytes(img_bytes)
    results = search_similar_vectors("images", features)
    return {"results": results}
