from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import text
from db.database import engine
from security import verify_password
from config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def authenticate_user(username, password):
    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT username, password, sector FROM users WHERE username=:u"),
            {"u": username}
        ).fetchone()

    if user and verify_password(password, user.password):
        return {"username": user.username, "sector": user.sector}
    return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload["sub"], "sector": payload["sector"]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
