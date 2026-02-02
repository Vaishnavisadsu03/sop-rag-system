from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = []
    for doc_id, doc in enumerate(documents):
        split_docs = splitter.split_documents([doc])
        for chunk in split_docs:
            chunk.metadata["doc_id"] = doc_id
            chunk.metadata["source"] = doc.metadata.get("source")
            chunk.metadata["plant"] = doc.metadata.get("plant")
            chunks.append(chunk)

    return chunks
