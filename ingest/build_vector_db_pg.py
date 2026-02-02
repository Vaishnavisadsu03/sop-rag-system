from sqlalchemy import create_engine, text
from config import DATABASE_URL
from ingest.load_sops import load_all_sops
from embeddings.embedding_model import get_embedding_model

engine = create_engine(DATABASE_URL)
embedder = get_embedding_model()

docs = load_all_sops()

with engine.begin() as conn:
    for doc in docs:
        embedding = embedder.embed_query(doc.page_content)

        conn.execute(
            text("""
                INSERT INTO sop_documents
                (plant, sop_name, sector, content, embedding)
                VALUES (:plant, :sop_name, :sector, :content, :embedding)
            """),
            {
                "plant": doc.metadata["plant"],
                "sop_name": doc.metadata["sop_name"],
                "sector": doc.metadata["sector"],
                "content": doc.page_content,
                "embedding": embedding
            }
        )

print("✅ SOPs indexed correctly with sector")
