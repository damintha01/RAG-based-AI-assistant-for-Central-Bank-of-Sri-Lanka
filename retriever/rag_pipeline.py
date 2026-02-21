import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from openai import OpenAI

# =============================
# Load Environment Variables
# =============================
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =============================
# Initialize Services
# =============================
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("rag-p1")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = OpenAI(api_key=OPENAI_API_KEY)

# =============================
# Retrieve Context
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
            "section_number": match["metadata"]["section_number"],
            "text": match["metadata"]["text"]
        })

    return retrieved_chunks


# =============================
# Build Prompt
# =============================
def build_prompt(query, retrieved_chunks):

    context = "\n\n".join([
        f"[Source: {chunk['document_name']} | Section: {chunk['section_number']}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    ])

    prompt = f"""
You are a regulatory compliance assistant for the Sri Lankan banking sector.

Answer strictly based on the provided context.
Do NOT use external knowledge.
If answer is not found, say "Information not available in provided documents."

Cite the source document and section number in your answer.

=====================
CONTEXT:
{context}
=====================

QUESTION:
{query}

Provide a clear and professional answer.
"""

    return prompt


# =============================
# Generate Answer
# =============================
def generate_answer(prompt):

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # cost-effective
        messages=[
            {"role": "system", "content": "You are a regulatory assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content


# =============================
# Full RAG Pipeline
# =============================
def ask(query):

    retrieved_chunks = retrieve_context(query)
    prompt = build_prompt(query, retrieved_chunks)
    answer = generate_answer(prompt)

    # Format sources
    sources = []
    for chunk in retrieved_chunks:
        sources.append({
            "document_name": chunk["document_name"],
            "section_number": chunk.get("section_number"),
            "page_number": None,  # Add if available
            "confidence_score": chunk["score"]
        })

    # Calculate overall confidence (average of top chunks)
    overall_confidence = sum(chunk["score"] for chunk in retrieved_chunks) / len(retrieved_chunks) if retrieved_chunks else 0.0

    return {
        "answer": answer,
        "sources": sources,
        "overall_confidence": overall_confidence
    }


# =============================
# Test
# =============================
if __name__ == "__main__":

    question = "What are capital adequacy requirements?"

    result = ask(question)

    print("\nFinal Answer:\n")
    print(result["answer"])
    print("\n\nSources:")
    for i, source in enumerate(result["sources"], 1):
        print(f"{i}. {source['document_name']} - Section {source['section_number']} (Score: {source['confidence_score']:.3f})")
    print(f"\nOverall Confidence: {result['overall_confidence']:.3f}")