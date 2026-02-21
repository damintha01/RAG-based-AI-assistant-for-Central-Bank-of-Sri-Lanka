import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone


# =============================
# Load Environment Variables
# =============================
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


# =============================
# Initialize Pinecone
# =============================
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "rag-p1"

# Check if index exists
try:
    index = pc.Index(index_name)
    # Test the connection
    index.describe_index_stats()
    print(f"✓ Connected to index '{index_name}'")
except Exception as e:
    print(f"✗ Error: Index '{index_name}' not found or inaccessible.")
    print(f"  Please run 'python ingestion/smart_ingest.py' first to create the index.")
    print(f"  Error details: {str(e)}")
    exit(1)


# =============================
# Load Embedding Model
# =============================
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# =============================
# Retrieval Function
# =============================
def retrieve_context(query: str, top_k: int = 5):

    query_embedding = embedding_model.encode(query).tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    retrieved_chunks = []

    for match in results["matches"]:
        retrieved_chunks.append({
            "score": match["score"],
            "document_name": match["metadata"]["document_name"],
            "section_number": match["metadata"].get("section_number", "Unknown"),
            "page_number": match["metadata"].get("page_number", "Unknown"),
            "text": match["metadata"]["text"]
        })

    return retrieved_chunks

# =============================
# Test Block
# =============================
if __name__ == "__main__":

    query = "What is CET1 ratio?"

    results = retrieve_context(query, top_k=5)

    for i, result in enumerate(results):
        print(f"\nResult {i+1}")
        print("Score:", result["score"])
        print("Document:", result["document_name"])
        print("Section:", result["section_number"])
        print("Page:", result["page_number"])
        print("Text:", result["text"][:400])