from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from auth.auth_service import authenticate_user, get_current_user
from security import create_access_token
from retrieval.retriever import retrieve_full_document
from schemas import SOPQuery

app = FastAPI(title="SOP Retrieval System")

# Serve UI
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return RedirectResponse(url="/ui/login.html")

# ---------------- LOGIN ----------------
@app.post("/login")
def login(data: dict):
    user = authenticate_user(data["username"], data["password"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["username"], user["sector"])
    return {"access_token": token}

# ---------------- SOP QUERY ----------------
@app.post("/query-sop")
def query_sop(data: SOPQuery, user=Depends(get_current_user)):
    result = retrieve_full_document(data.query, user["sector"])
    if not result:
        raise HTTPException(status_code=404, detail="No SOP found")

    return {
        "plant": result.plant,
        "sop_name": result.sop_name,
        "content": result.content,
        "distance": result.distance
    }

# ---------------- HEALTH ----------------
@app.get("/health")
def health():
    return {"status": "running"}
