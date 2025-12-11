"""
Book Collection Management API

A FastAPI application for managing a personal book collection using SQLAlchemy ORM and SQLite.
Allows users to add, view, update, delete, and search books.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from pydantic import BaseModel
from typing import List, Optional

# --- Database Configuration ---
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- New Declarative Base (SQLAlchemy 2.0 style) ---
class Base(DeclarativeBase):
    pass

# --- Pydantic Models (Pydantic V2 compatible) ---
class BookBase(BaseModel):
    """Base model for book data."""
    title: str
    author: str
    year: Optional[int] = None

class BookCreate(BookBase):
    """Model for creating a new book."""
    pass

class BookUpdate(BookBase):
    """Model for updating an existing book."""
    pass

class Book(BookBase):
    """Model for returning book data, including ID."""
    id: int

    class Config:
        from_attributes = True  # ← заменено orm_mode на from_attributes

# --- SQLAlchemy ORM Model ---
class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)

# --- Dependency for Database Session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Initialize FastAPI App ---
app = FastAPI(
    title="Book Collection API",
    description="An API to manage your personal book collection.",
    version="1.0.0"
)

# --- Create tables ---
Base.metadata.create_all(bind=engine)

# --- API Endpoints ---
@app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookModel(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(BookModel).offset(skip).limit(limit).all()
    return books

@app.get("/books/search/", response_model=List[Book])
def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BookModel)
    if title:
        query = query.filter(BookModel.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(BookModel.author.ilike(f"%{author}%"))
    if year is not None:
        query = query.filter(BookModel.year == year)
    return query.all()

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return None

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}

# --- Main entry point ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)