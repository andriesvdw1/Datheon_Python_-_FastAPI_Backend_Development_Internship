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
            detail="email or password is invalid"
            headers={"WWW-Authenticate", "Bearer"},
        )
    return{"message": "Login successful"}
