# tests/services/test_books.py
import pytest
from sqlalchemy.orm import Session
from src.models.books import Book
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.api.schemas.books import BookCreate, BookUpdate


def test_create_book(db_session: Session):
    repo = BookRepository(Book, db_session)
    service = BookService(repo)

    book_in = BookCreate(
        title="The Test Book",
        author="Author Name",
        description="A test book for unit tests."
    )

    book = service.create(obj_in=book_in)

    assert book.title == "The Test Book"
    assert book.author == "Author Name"
    assert book.description == "A test book for unit tests."


def test_update_book(db_session: Session):
    repo = BookRepository(Book, db_session)
    service = BookService(repo)

    book = service.create(BookCreate(title="Original", author="Author", description="Desc"))
    updated = service.update(book, BookUpdate(title="Updated"))

    assert updated.title == "Updated"
    assert updated.id == book.id


def test_delete_book(db_session: Session):
    repo = BookRepository(Book, db_session)
    service = BookService(repo)

    book = service.create(BookCreate(title="To Delete", author="Author", description="Desc"))
    service.remove(id=book.id)

    assert service.get(book.id) is None
