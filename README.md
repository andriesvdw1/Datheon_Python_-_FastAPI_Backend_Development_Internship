# Datheon Python - FastAPI Backend Development Internship  
Application ID: DT-2026-X897O  
Intern Full Name: Andries Van Der Westhuizen
## Task1 Name: BookStore REST API with Pydantic Validation
## Task1 Detailed Problem Statement and Requirements:
Implement a clean RESTful API using FastAPI and Pydantic schemas for request validation, query filtering and automatic Swagger docs.

## TechStack / Tools used:
FastAPI, Uvicorn, Pydantic and Python 3.

## Technical Approach

### Step 1: Planning the Book model in English first:
Each book should store the details about the specific book including:
The ISBN(International Standard Book Number) code which is a combination of a 13 digit or 10 digits number. 
The title of the book.
The publisher name of the company that published the book.
The publication year in which the book was published.
The price of the book.
The author or authors of the book.
The quantity of stock available for the specific book as a number between 0 and 1000.

### Define Pydantic models for Book schema
```python
from decimal import Decimal
from pydantic import BaseModel, Field

class Book(BaseModel):
  isbn: str = Field(min_lenght=10, max_length=13, description="10 or 13-digit ISBN code")
  title: str = Field(min_length=1, max_length=255)
  author: str = Field(min_length=1, max_length=100)
  publisher: str = Field(min_length= 1, max_length= 35)
  year_published: int = Field(ge=1000, le=2100, description="Year of publication")
  price: Decimal= Field(ge=Decimal("0.00"), description="The price of the book in Dollars"
  stock_quantity: int = Field(ge=0, le=1000)  
```

### Step 2: Implement GET, POST, PUT, DELETE endpoints
Create a file called app.py that will act as the server and will contain the HTTP endpoints used to create, read, update or delete book information from the system.
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="BookStore REST API with Pydantic Validation")
app.get("/")
def root():
  return{"service" : "BookStore REST API", "status" : "ok"}
```

### Add proper HTTP status codes and error handling to the endpoints

## Expected Deliverable:
Running local API server with interactive Swagger UI (/docs) testing all CRUD operations.
