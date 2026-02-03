🔹 What is this project?

In many organizations, Standard Operating Procedures (SOPs) are stored as text files or PDFs.
Finding the right SOP using keyword search is difficult and inefficient.
This project solves that problem by building a Semantic SOP Retrieval System using AI embeddings and vector search.
👉Instead of matching keywords, the system understands the meaning of the query and finds the most relevant SOP.

🔹 What does this system do?

✔ User logs in securely
✔ User asks a question in natural language
✔ System finds the most relevant SOP using semantic similarity
✔ SOP access is restricted by department/sector
✔ Results are shown in a simple web UI

Example:

Query: “How to restart the IT server safely?”
Result: Returns the correct IT department SOP even if the words don’t exactly match.

🔹 Tech Stack Used

1. Backend: FastAPI (Python)
2. Database: PostgreSQL
3. Vector Search: pgvector
4. Embeddings: Sentence Transformers
5. Authentication: JWT (JSON Web Token)
6. Frontend: HTML, CSS, JavaScript
7. ORM / DB Access: SQLAlchemy

🔹 How the system works (Step by Step)

1️⃣ SOP Ingestion (One-time process)
SOP files are stored in folders like:
✔ sop_data/
  └── Plant_A/
      └── IT_Department/
          └── SOP_001.txt
✔ Each SOP is:
    Read from file
    Converted into embedding vectors
    Stored in PostgreSQL using pgvector
    
2️⃣ User Login

✔ User logs in using username & password
✔ Backend verifies credentials
✔ A JWT token is generated
✔ Token contains the user’s sector/department

3️⃣ SOP Query

✔ User types a question in the UI
✔ Backend:
    1. Converts the query into an embedding
    2. Performs vector similarity search
    3. Filters SOPs based on user’s sector
    4. Returns the most relevant SOP

4️⃣ Result Display

✔ UI shows:
    SOP name
    SOP content
    Similarity distance score
    
🔹 Why not keyword search?

✔ Keyword Search	                    ✔ Semantic Search (This Project)
Exact word match	                    Meaning-based match
Misses relevant SOPs	                Finds correct SOP
Poor user experience	                Intelligent search
No context	                          Understands intent

🔹 How to Run the Project

1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Initialize the database
python -m db.init_db

3️⃣ Ingest SOPs
python -m ingest.build_vector_db_pg

4️⃣ Start the server
uvicorn main:app --reload

5️⃣ Open browser
http://127.0.0.1:8000/

🔹 Key Features

✔ Semantic SOP search using embeddings
✔ Sector-based access control
✔ Secure authentication with JWT
✔ Fast retrieval using pgvector
✔ Clean and simple UI

🔹 Challenges Solved (Important)

 1. pgvector type casting issues
 2. SQLAlchemy + PostgreSQL compatibility
 3. Embedding consistency
 4. Metadata-based filtering
 5. Secure authentication flow

🔹 Conclusion

This project demonstrates a real-world AI-powered information retrieval system using modern backend technologies.
It goes beyond basic CRUD and shows how semantic search can be applied in enterprise systems.
