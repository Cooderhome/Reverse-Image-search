from elasticsearch import Elasticsearch
import numpy as np

es = Elasticsearch("http://localhost:9200")

# Test the connection
if es.ping():
    print("Successfully connected to Elasticsearch!")
else:
    print("Could not connect to Elasticsearch.")
def search_similar_vectors(index, query_vector, top_k=5):
    script_query = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }
    res = es.search(index=index, body=script_query)
    return [
        {
            "id": hit["_id"],
            "score": hit["_score"],
            "file_name": hit["_source"]["metadata"]["file_name"]
        }
        for hit in res["hits"]["hits"]
    ]
