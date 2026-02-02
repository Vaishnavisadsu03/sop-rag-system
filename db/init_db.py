from sqlalchemy import text
from db.database import engine
from config import EMBEDDING_DIM

def initialize_database():
    with engine.begin() as conn:
        print("🛠️ Enabling pgvector extension...")
        # Required for the VECTOR data type to work
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

        print("🏗️ Creating tables...")
        # User table for sector-based access control
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                sector TEXT
            );
        """))

        # Main document table for RAG
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS sop_documents (
                id SERIAL PRIMARY KEY,
                plant TEXT,
                sop_name TEXT,
                sector TEXT,
                content TEXT,
                embedding VECTOR({EMBEDDING_DIM})
            );
        """))

        # Audit logs for tracking queries
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id SERIAL PRIMARY KEY,
                username TEXT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        print("⚡ Creating HNSW index for fast vector search...")
        # Speeds up Cosine Similarity searches
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_sop_embedding 
            ON sop_documents USING hnsw (embedding vector_cosine_ops);
        """))

    print("✅ Database fully initialized and indexed.")

if __name__ == "__main__":
    initialize_database()