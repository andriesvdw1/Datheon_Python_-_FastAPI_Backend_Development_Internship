# Task 2 User Authentication & RBAC with JWT
Secure FastAPI endpoints with JSON Web Tokens and password hashing.

# Detailed problem statement and requirements
Create user registration and login endpoints that issue signed JWT tokens using passlib/bcrypt, and protect sensitive routes via Depends(get_current_user).

# Technical Approach
Implement OAuth2PasswordBearer security scheme, hash passwords with bcrypt, verify tokens and extract claims in route dependencies.

# Tools
FastAPI, python-jose, passlib[bcrypt]

# Expected Deliverable: Secured API endpoints rejecting unauthorized calls and returning protected data for authenticated users.