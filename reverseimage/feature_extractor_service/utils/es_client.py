import uuid
from elasticsearch import Elasticsearch


# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Test the connection
if es.ping():
    print("Successfully connected to Elasticsearch!")
else:
    print("Could not connect to Elasticsearch.")
def create_index_if_not_exists(index_name, dims=512):
    try:
        if not es.indices.exists(index=index_name):
            print(f"📦 Creating index: {index_name}")
            mapping = {
                "mappings": {
                    "properties": {
                        "vector": {
                            "type": "dense_vector",
                            "dims": dims
                        },
                        "metadata": {
                            "properties": {
                                "file_name": {"type": "keyword"}
                            }
                        }
                    }
                }
            }
            es.indices.create(index=index_name, body=mapping)
        else:
            print(f"✔️ Index '{index_name}' already exists")
    except Exception as e:
        print(f"❌ Error while checking/creating index: {e}")

# --- Index a document (feature vector + metadata) ---
def index_feature_vector(index, doc_id, vector, metadata):
    doc = {
        "vector": vector,
        "metadata": metadata
    }
    try:
        res = es.index(index=index, id=doc_id, document=doc)
        print("📥 Document indexed successfully:", res)
    except :
        print("❌ Failed to index document:", )
