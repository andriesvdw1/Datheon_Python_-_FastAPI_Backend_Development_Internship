from fastapi import FastAPI, Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta

# Configuration and setup of in-memory database
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# instantiate an instance of FastAPI
app = FastAPI()

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory database
memory_users_db = {}

# Create the FASTAPI endpoints for a user to register and login

# Define that a user has a email and password
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Define the User login pydantic model
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Define the Token pydantic model
class Token(BaseModel):
    access_token: str
    token_type: str

# hash password function
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password function to check hashed password with unhashed password
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

# Function to create a new access token
def new_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# User registration endpoint
@app.post("/register", status_code=status.HTTP_201_CREATED)
def new_user_register(user: UserCreate):
    if user.email in memory_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use for a user"
        )

    # Use a hashed password for security purposes
    hashed_password = hash_password(user.password)
    memory_users_db[user.email] = {
        "email": user.email,
        "hashed_password": hashed_password
    }

    # Inform user on the successful user registration
    return {"message": "User registration successful", "email": user.email}

# User login endpoint
@app.post("/login", response_model=Token)
def user_login(user: UserLogin):
    db_user = memory_users_db.get(user.email)

    # Check if the user exists in the in-memory database
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="email or password is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # access for a token will expire after 30 minutes
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = new_access_token(
        data = {"sub" : user.email}, expires_delta=access_token_expires
    )
    return{"access_token": access_token, "token_type": "bearer"}
