# Datheon Python - FastAPI Backend Development Internship  
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
The collection of books will be stored in a Python dictionary.
Every time a book is added to the books collection the id value of the new book increases by 1.

### Define Pydantic models for Book schema
```python
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class Book(BaseModel):
  isbn: str = Field(min_length=10, max_length=13, description="10 or 13-digit ISBN code")
  title: str = Field(min_length=1, max_length=255)
  author: str = Field(min_length=1, max_length=100)
  publisher: str = Field(min_length= 1, max_length= 35)
  year_published: int = Field(ge=1000, le=2100, description="Year of publication")
  price: Decimal= Field(ge=Decimal("0.00"), description="The price of the book in Dollars")
  stock_quantity: int = Field(ge=0, le=1000)

class BookUpdate(BaseModel):
  isbn: Optional[str] = Field(default=None,min_length=10, max_length=13, description="10 or 13-digit ISBN code")
  title: Optional[str] = Field(default=None,min_length=1, max_length=255)
  author: Optional[str] = Field(default=None,min_length=1, max_length=100)
  publisher: Optional[str] = Field(default=None,min_length= 1, max_length= 35)
  year_published: Optional[int] = Field(default=None,ge=1000, le=2100, description="Year of publication")
  price: Optional[Decimal] = Field(default=None,ge=Decimal("0.00"), description="The price of the book in Dollars")
  stock_quantity: Optional[int] = Field(default=None,ge=0, le=1000)
```

### Step 2: Implement GET, POST, PUT, DELETE endpoints with status codes and validation
Create a file called app.py that will act as the server and will contain the HTTP endpoints used to create, read, update or delete book information from the system.
```python
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="BookStore REST API with Pydantic Validation")
# code to confirm that the server is running
@app.get("/")
def root():
  return{"service" : "BookStore REST API", "status" : "ok"}

class BookOut(Book):
  id: int

books :dict[int, BookOut] = {}
next_id = 1

# code to create a new book and add it to the collection of books
@app.post("/books", response_model=BookOut, status_code=201)
def create_book(book: Book):
  global next_id
  stored = BookOut(id=next_id, **book.model_dump())
  books[next_id] = stored
  next_id += 1
  return stored

# code to get a book by id value, if the book is in the collection
@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int):
  if book_id not in books:
    raise HTTPException(status_code=404, detail="Book is not found, perhaps the incorrect book id number was entered.")
  return books[book_id]

# code to update a book that already exists in the collection
@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_update: BookUpdate):
  if book_id not in books:
    raise HTTPException(status_code=404, detail="Book is not found, perhaps the incorrect book id number was entered.")
  existing_book = books[book_id]
  #update the changed field values for the specified book
  update_data = book_update.model_dump(exclude_unset=True)
  updated_book_data = existing_book.model_copy(update=update_data)

  books[book_id] = updated_book_data
  return updated_book_data

# code to remove a book from the books collection
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id : int):
  if book_id not in books:
    raise HTTPException(status_code=404, detail="Book with specified book id value not found")
  del books[book_id]
```

### Step 3: Create a Python virtual environment and install dependencies
Command to run in command prompt on Windows:
```
python -m venv venv
cd venv
cd Scripts
activate.bat
pip install fastapi uvicorn pydantic
```
Command to start the server:
first change the current directory by moving up two folders.
```
cd ../
cd ../
python -m uvicorn server:app --reload
```
Open the web browser and navigate to: http://127.0.0.1:8000/
The result that shows in the browser is:
{"service":"BookStore REST API","status":"ok"}

### Step 4: Create a Client to interact with the server
With the command prompt still open press the ctrl + c buttons on the
keyboard to stop the server.
With the virtual environment (venv) still open run the following command to install the httpx package that will be required for the 
client:
```
pip install httpx
``` 
## Contents of client.py file:
```python
import httpx

BASE = "http://127.0.0.1:8000"

books = [
	{"isbn" : "9781801116022","title": "python programming crash course", "author": "Tony F Charles ","publisher": "Tony F. Charles", "year_published": 2020, "price" : 28.75, "stock_quantity" : 1},
]

add_book = [
	{"isbn" : "9781593279929","title":"Automate The Boring Stuff With Python, 2nd Edition", "author": "Al Sweigart", "publisher": "No Starch Press,US", "year_published": 2019, "price" : 54.63, "stock_quantity" : 5},
]

for book in books:
	r = httpx.post(f"{BASE}/books", json=book)
	print(r.status_code, r.json())

for book in add_book:
	r = httpx.post(f"{BASE}/books", json=book)
	print(r.status_code, r.json())
```
### Testing that the client adds the book to the server:
In command prompt run the command to start the server:
```
python -m uvicorn server:app --reload
```
In a different command prompt run the command to start the client:
python client.py

Output recieved command prompt shows success:
```
201 {'isbn': '9781801116022', 'title': 'python programming crash course', 'author': 'Tony F Charles ', 'publisher': 'Tony F. Charles', 'year_published': 2020, 'price': '28.75', 'stock_quantity': 1, 'id': 1}
201 {'isbn': '9781593279929', 'title': 'Automate The Boring Stuff With Python, 2nd Edition', 'author': 'Al Sweigart', 'publisher': 'No Starch Press,US', 'year_published': 2019, 'price': '54.63', 'stock_quantity': 5, 'id': 2}
```

Output on the command prompt of the server shows success:
```
INFO:     127.0.0.1:53175 - "POST /books HTTP/1.1" 201 Created
```
## Expected Deliverable:
Running local API server with interactive Swagger UI (/docs) testing all CRUD operations.
