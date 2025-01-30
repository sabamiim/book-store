from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import schemas

from file import models

router = APIRouter()

@router.post("/create-book", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(models.get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/get-book", response_model=list[schemas.BookOut])
def get_books(db: Session = Depends(models.get_db)):
    return db.query(models.Book).all()

@router.put("/update-book{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(models.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/delete-book{book_id}")
def delete_book(book_id: int, db: Session = Depends(models.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
