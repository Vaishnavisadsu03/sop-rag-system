from langchain_community.vectorstores import FAISS  # ✅ FIXED
from ingest.load_sops import load_all_sops
from ingest.chunk_sops import chunk_documents
from embeddings.embedding_model import get_embedding_model
from config import VECTOR_DB_PATH


def build_vector_database():
    documents = load_all_sops()
    chunks = chunk_documents(documents)
    embedding_model = get_embedding_model()

    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    vector_db.save_local(VECTOR_DB_PATH)
    print("✅ Vector DB built successfully")


if __name__ == "__main__":
    build_vector_database()
