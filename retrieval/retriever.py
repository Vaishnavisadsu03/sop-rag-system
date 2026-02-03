from sqlalchemy import text
from db.database import engine
from embeddings.embedding_model import get_embedding_model

embedder = get_embedding_model()

def retrieve_full_document(query: str, sector: str):
    # Generate the embedding vector from the query string
    embedding = embedder.embed_query(query)

    # Convert list to pgvector string format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"

    # Use CAST to avoid the SQLAlchemy double-colon syntax error
    sql = """
    SELECT plant, sop_name, content,
           (embedding <=> CAST(:emb AS vector)) AS distance
    FROM sop_documents
    WHERE sector = :sec
    ORDER BY distance
    LIMIT 1
    """

    with engine.connect() as conn:
        # Pass both 'emb' and 'sec' in the parameters dictionary
        result = conn.execute(
            text(sql),
            {
                "emb": embedding_str,
                "sec": sector
            }
        ).fetchone()
        
        return result