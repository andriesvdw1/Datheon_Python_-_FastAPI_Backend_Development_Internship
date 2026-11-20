# Task 2 User Authentication & RBAC with JWT
Secure FastAPI endpoints with JSON Web Tokens and password hashing.

# Detailed problem statement and requirements
Create user registration and login endpoints that issue signed JWT tokens using passlib/bcrypt, and protect sensitive routes via Depends(get_current_user).

# Dependencies to be installed using the command:
pip install fastapi uvicorn "passlib[bcrypt]" python-jose[cryptography] pydantic email-validator

# Technical Approach
Implement OAuth2PasswordBearer security scheme, hash passwords with bcrypt, verify tokens and extract claims in route dependencies.

# Tools
FastAPI, python-jose, passlib[bcrypt]
# Command to run the server:
```
python -m uvicorn task2:app --reload
```

# Command to run the tests:
```
python -m pytest -s test_task2.py
```

# Expected Deliverable: Secured API endpoints rejecting unauthorized calls and returning protected data for authenticated users.
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\Admin\Downloads\Datheon_Python_-_FastAPI_Backend_Development_Internship-main (3)\Datheon_Python_-_FastAPI_Backend_Development_Internship-main\Task 2
plugins: anyio-4.15.1, logfire-5.2.0, platformdirs-4.13.5
collected 6 items

test_task2.py
[TEST] Registering user with payload: {'email': 'test@example.com', 'password': 'strongpassword123'}
-> Response Status: 201
-> Response Body: {'message': 'User registration successful', 'email': 'test@example.com'}
.
[TEST] Registering initial user: {'email': 'test@example.com', 'password': 'strongpassword123'}
[TEST] Attempting duplicate registration with same payload: {'email': 'test@example.com', 'password': 'strongpassword123'}
-> Response Status: 400
-> Response Body: {'detail': 'Email already in use for a user'}
.
[TEST] Logging in user with credentials: {'username': 'test@example.com', 'password': 'strongpassword123'}
-> Response Status: 200
-> Response Body: {'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzk1MjA2NzkwfQ.xs7jbfJ91ef4GhfoGt2xK-zuR8KwYUxHGMGP8JrEo_s', 'token_type': 'bearer'}
.
[TEST] Logging in with wrong password: {'username': 'test@example.com', 'password': 'wrongpassword'}
-> Response Status: 401
-> Response Body: {'detail': 'email or password is invalid'}

[TEST] Logging in with non-existent user: {'username': 'nonexistent@example.com', 'password': 'strongpassword123'}
-> Response Status: 401
-> Response Body: {'detail': 'email or password is invalid'}
.
[TEST] Accessing protected route /users/me with token acquired for: test@example.com
-> Response Status: 200
-> Response Body: {'email': 'test@example.com'}
.
[TEST] Accessing protected route /users/me without any token
-> Response Status: 401

[TEST] Accessing protected route /users/me with invalid/malformed token
-> Response Status: 401
.

============================================================================================== 6 passed in 2.26s ===============================================================================================

