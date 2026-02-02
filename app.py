from fastapi import FastAPI, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from jose import jwt, JWTError
from sqlalchemy import create_engine, text

from config import SECRET_KEY, ALGORITHM, DATABASE_URL
from auth.auth_service import authenticate_user
from security import create_access_token
from retrieval.retriever import retrieve_full_document

# -------------------------------------------------
# APP INITIALIZATION
# -------------------------------------------------

app = FastAPI(
    title="Industry SOP Retrieval System",
    version="1.0"
)

# -------------------------------------------------
# UI SETUP
# -------------------------------------------------

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------------------------------
# DATABASE
# -------------------------------------------------

engine = create_engine(DATABASE_URL)

# -------------------------------------------------
# AUTH
# -------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # {username, sector}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# -------------------------------------------------
# UI ROUTE
# -------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# -------------------------------------------------
# LOGIN API
# -------------------------------------------------

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "username": user["username"],
        "sector": user["sector"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -------------------------------------------------
# SOP QUERY API (SECTOR PROTECTED)
# -------------------------------------------------

@app.get("/query")
def query_sop(
    question: str = Query(..., description="User SOP question"),
    user=Depends(get_current_user)
):
    """
    Only SOPs belonging to user's sector will be retrieved
    """

    result = retrieve_full_document(
        query=question,
        sector=user["sector"]
    )

    if not result:
        raise HTTPException(status_code=404, detail="No SOP found")

    # Audit log
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO audit_logs (username, action)
                VALUES (:u, :a)
            """),
            {
                "u": user["username"],
                "a": f"SOP query: {question}"
            }
        )

    return {
        "plant": result["plant"],
        "source": result["source"],
        "confidence_score": result["confidence_score"],
        "content": result["content"]
    }

# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------

@app.get("/health")
def health():
    return {"status": "running"}
