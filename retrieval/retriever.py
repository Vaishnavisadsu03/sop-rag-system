from sqlalchemy import text
from db.database import engine
from embeddings.embedding_model import get_embedding_model

embedder = get_embedding_model()

def retrieve_full_document(query: str, sector: str):
    query_embedding = embedder.embed_query(query)
    # Using <=> for Cosine Similarity
    sql = """
        SELECT plant, sop_name, content, (embedding <=> :emb) as distance
        FROM sop_documents WHERE sector = :sec
        ORDER BY distance ASC LIMIT 1
    """
    with engine.connect() as conn:
        row = conn.execute(text(sql), {"emb": query_embedding, "sec": sector}).fetchone()
    return row