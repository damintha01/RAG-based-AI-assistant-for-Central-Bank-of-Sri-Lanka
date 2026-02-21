import os
import json
import re
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

# =============================
# Load environment variables
# =============================
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# =============================
# Initialize Pinecone
# =============================
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "rag-p1"

if index_name not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

# =============================
# Load embedding model
# =============================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =============================
# Smart Section Splitter
# =============================
def split_by_sections(text):
    pattern = r"(Section\s+\d+.*?|Regulation\s+\d+.*?|Article\s+\w+.*?)(?=Section\s+\d+|Regulation\s+\d+|Article\s+\w+|$)"
    matches = re.findall(pattern, text, flags=re.DOTALL)
    return matches if matches else [text]

def extract_section_number(section_text):
    match = re.search(r"(Section\s+\d+(\.\d+)*)", section_text)
    return match.group(1) if match else "Unknown"

# =============================
# Chunk large sections
# =============================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200
)

# =============================
# Process ALL documents
# =============================
PROCESSED_PATH = "data/processed/"

vector_id_counter = 0
batch = []
batch_size = 100

for file in os.listdir(PROCESSED_PATH):

    if not file.endswith(".json"):
        continue

    print(f"Processing {file}")

    file_path = os.path.join(PROCESSED_PATH, file)

    with open(file_path, "r", encoding="utf-8") as f:
        pages = json.load(f)

    document_name = file.replace(".json", "")

    # Detect regulation type
    if "AR_" in file:
        regulation_type = "Annual_Report"
    elif "fsr" in file.lower():
        regulation_type = "Financial_Stability_Report"
    elif "monetary" in file.lower():
        regulation_type = "Monetary_Policy"
    elif "monthly" in file.lower():
        regulation_type = "Monthly_Bulletin"
    else:
        regulation_type = "Other"

    # Combine pages
    full_text = ""
    for page in pages:
        full_text += page["text"] + "\n"

    # Smart section split
    sections = split_by_sections(full_text)

    for section in sections:

        section_number = extract_section_number(section)

        # Further split large sections
        sub_chunks = splitter.split_text(section)

        for sub_id, chunk_text in enumerate(sub_chunks):

            embedding = model.encode(chunk_text).tolist()

            metadata = {
                "document_name": document_name,
                "regulation_type": regulation_type,
                "section_number": section_number,
                "sub_chunk_id": sub_id,
                "text": chunk_text
            }

            batch.append({
                "id": f"vec-{vector_id_counter}",
                "values": embedding,
                "metadata": metadata
            })

            vector_id_counter += 1

            # Upload in batches
            if len(batch) >= batch_size:
                index.upsert(vectors=batch)
                batch = []

# Upload remaining
if batch:
    index.upsert(vectors=batch)

print("All documents successfully uploaded to Pinecone!")