import httpx

BASE = "http://127.0.0.1:8000"

books = [
	{"isbn" : "9781801116022","title": "python programming crash course", "author": "Tony F Charles ","publisher": "Tony F. Charles", "year_published": 2020, "price" : 28,75, "stock_quantity" : 1},
]

for book in books:
	r = httpx.post(f"{BASE}/books", json=book)
	print(r.status_code, r.json())