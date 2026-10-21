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