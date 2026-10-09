
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import Base, engine, get_db
import models
import schemas

# Create tables (Vault initialization) - creates memory_vault.db file
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Decode Labs Project 2 - Memory Vault")

@app.get("/", status_code=200)
def root():
    return {"message": "Memory Vault is online - Persistence IPO Model active"}

# INPUT -> PROCESS -> OUTPUT
@app.post("/users", status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(email=user.email, age=user.age)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig).lower() if hasattr(e, 'orig') else str(e).lower()
        if "unique" in error_msg or "already exists" in error_msg or "duplicate" in error_msg:
            raise HTTPException(
                status_code=409,
                detail=f"Conflict: Email '{user.email}' already exists in Vault."
            )
        if "check" in error_msg or "age" in error_msg:
            raise HTTPException(status_code=400, detail="Check violation: age must be >= 0")
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")

@app.get("/users", status_code=200)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"count": len(users), "data": users}

@app.get("/users/{user_id}", status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None
