from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Configuration and setup
SECRET_KEY = "260a064799c1b4df21279a0a70fd9c537b49c356e3939b0927a1db9df5c2d8ef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create an instance of FastAPI
app = FastAPI()

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory database
memory_users_db = {}


# Pydantic Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Helper Functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def new_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# User Registration Endpoint
@app.post("/register", status_code=status.HTTP_201_CREATED)
def new_user_register(user: UserCreate):
    if user.email in memory_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use for a user",
        )

    hashed_password = hash_password(user.password)
    memory_users_db[user.email] = {
        "email": user.email,
        "hashed_password": hashed_password,
    }

    return {"message": "User registration successful", "email": user.email}


# User Login Endpoint
@app.post("/login", response_model=Token)
def user_login(user: UserLogin):
    db_user = memory_users_db.get(user.email)

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="email or password is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = new_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Protected Route Endpoint
@app.get("/users/me")
def find_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
