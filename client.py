import httpx

BASE = "http://127.0.0.1:8000"

books = [
	{"isbn" : "9781801116022","title": "python programming crash course", "author": "Tony F Charles ","publisher": "Tony F. Charles", "year_published": 2020, "price" : 28.75, "stock_quantity" : 1},
]

add_book = [
	{"isbn" : "9781593279929","title":"Automate The Boring Stuff With Python, 2nd Edition", "author": "Al Sweigart", "publisher": "No Starch Press,US", "year_published": 2019, "price" : 54.63, "stock_quantity" : 5},
	{"isbn" : "9781337102100","title":"Microsoft Visual C# 2017: An Introduction to Object-Oriented Programming", "author": "Joyce Farrell", "publisher": "Cengage Learning", "year_published": 2017, "price" : 213.65, "stock_quantity" : 1},
]
print("===================Available books:============================")
for book in books:
	r = httpx.post(f"{BASE}/books", json=book)
	print(r.status_code, r.json())

for book in add_book:
	r = httpx.post(f"{BASE}/books", json=book)
	print(r.status_code, r.json())

print("==============================================================")

print("===================Updated book:============================")
# update one specific book by using the book id to reduce the price
url =  "http://127.0.0.1:8000/books/3"
payload = {"isbn" : "9781337102100","title":"Microsoft Visual C# 2017: An Introduction to Object-Oriented Programming", "author": "Joyce Farrell", "publisher": "Cengage Learning", "year_published": 2017, "price" : 200.00, "stock_quantity" : 1}

r = httpx.put(url, json=payload)
print(r.status_code)
print(r.json())
print("===========================================================")

