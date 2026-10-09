# Decode Labs Project 2 - The Memory Vault (Persistence IPO Model)

This is the upgrade from Project 1: From transient `user_db = []` to permanent commercial-grade storage.

## Concepts from PDF

1. **The Vault's Immune System: Data Integrity**
   - `email: UNIQUE + NOT NULL` -> Rejected by NOT NULL if missing, Rejected by UNIQUE if duplicate
   - `age: CHECK (age >= 0) + NOT NULL` -> Rejected by CHECK if -5

2. **Handling the Breach: HTTP 409 Conflict**
   Request -> Vault Check (UNIQUE violation) -> ORM Intercept (IntegrityError/P2002) -> Response Translation -> 409 Conflict
   RFC 7231: The request could not be completed due to conflict with current state.

3. **Synthesis: Persistence IPO Model**
   INPUT (Client Domain): HTTP POST / JSON transient and untrusted
   PROCESS (Server Domain): API Route + ORM sanitizes + Gatekeeper checks 409
   OUTPUT (Storage Domain): Postgres commits permanent row to disk

## Setup - Step 1: Local Configuration

### Option A: Postgres with Docker (Recommended as per PDF)
```bash
docker-compose up -d
```
Create .env file:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/memory_vault
```

### Option B: Quick test without Docker (SQLite)
Just run without .env, it will use `memory_vault.db` file automatically. Same constraints work.

### Install & Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Verification - Step 2: CRUD Lifecycle Test (Postman)

As per PDF page "Verification: The Gatekeeper Rule"

1. **POST to create user (Verify 201)**
   POST http://127.0.0.1:8000/users
   Body: {"email": "a@b.com", "age": 24}
   -> Expect 201 Created

2. **POST exact same user (Verify 409 Conflict)**
   Same body again
   -> Expect 409 Conflict - "Email 'a@b.com' already exists"

3. **POST invalid data (Verify Immune System)**
   {"email": "a@b.com", "age": -5} -> 400 / 422 CHECK fails
   {"age": 24} -> 422 NOT NULL (missing email)

4. **GET list to confirm persistence (Verify 200)**
   GET http://127.0.0.1:8000/users
   -> Expect 200, count=1, data persists even after restart (if Postgres)

5. **DELETE to clean state (Verify 204)**
   DELETE http://127.0.0.1:8000/users/1
   -> Expect 204 No Content

## Git Submission (Same as Project 1)
```bash
git add .
git commit -m "feat: Implement Memory Vault with Postgres, UNIQUE constraint and 409 handling"
git push
```

