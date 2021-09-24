from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import operations.crud as opcrud
import operations.models as opmod
import operations.schemas as opsch
from operations.database import SessionLocal, engine

opmod.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=opsch.User)
def create_user(user: opsch.UserCreate, db: Session = Depends(get_db)):
    db_user = opcrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return opcrud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[opsch.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = opcrud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=opsch.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = opcrud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=opsch.Item)
def create_item_for_user(
    user_id: int, item: opsch.ItemCreate, db: Session = Depends(get_db)
):
    return opcrud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[opsch.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = opcrud.get_items(db, skip=skip, limit=limit)
    return items
