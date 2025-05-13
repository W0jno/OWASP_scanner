from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
import db.models, db.schemas


app = FastAPI()

db.models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "dupa"}

@app.post("/users/", response_model=db.schemas.UserOut)
def create_user(user: db.schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(db.models.User).filter(db.models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=db.schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db.models.User).filter(db.models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user