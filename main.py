from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth_service import authenticate_user, get_current_user
from security import create_access_token
from retrieval.retriever import retrieve_full_document
from schemas import SOPQuery

app = FastAPI()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user: raise HTTPException(status_code=401, detail="Invalid login")
    token = create_access_token(user["username"], user["sector"])
    return {"access_token": token, "token_type": "bearer"}

@app.post("/query-sop")
async def query(data: SOPQuery, user=Depends(get_current_user)):
    result = retrieve_full_document(data.query, user["sector"])
    if not result: raise HTTPException(status_code=404, detail="Not found")
    return {"plant": result.plant, "content": result.content}