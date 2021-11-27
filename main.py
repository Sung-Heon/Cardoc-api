from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/auth/register", response_model=schemas.User)
def create_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_register_id(db, register_id=user.register_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@app.get("/auth/login", response_model=schemas.UserRegister)
def login(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_register_id(db, register_id=user.register_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")


    return db_user

