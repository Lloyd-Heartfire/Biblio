import pytest
from sqlalchemy.orm import Session

from src.models.users import User
from src.models.books import Book
from src.models.loans import Loan
from src.repositories.users import UserRepository
from src.repositories.books import BookRepository
from src.repositories.loans import LoanRepository
from src.services.users import UserService
from src.services.books import BookService
from src.services.loans import LoanService
from src.api.schemas.users import UserCreate
from src.api.schemas.books import BookCreate
from src.api.schemas.loans import LoanCreate


@pytest.fixture
def setup_user_and_book(db_session: Session):
    """
    Prépare un utilisateur et un livre pour les tests d'emprunt.
    """
    user_repo = UserRepository(User, db_session)
    book_repo = BookRepository(Book, db_session)

    user_service = UserService(user_repo)
    book_service = BookService(book_repo)

    user = user_service.create(UserCreate(
        email="loanuser@example.com",
        password="securepassword",
        full_name="Loan User",
        is_active=True,
        is_admin=False
    ))

    book = book_service.create(BookCreate(
        title="Loanable Book",
        author="Author Test",
        description="Book ready to be loaned."
    ))

    return user, book


def test_create_loan(db_session: Session, setup_user_and_book):
    """
    Teste la création d’un emprunt.
    """
    user, book = setup_user_and_book
    loan_repo = LoanRepository(Loan, db_session)
    loan_service = LoanService(loan_repo)

    loan_in = LoanCreate(user_id=user.id, book_id=book.id)
    loan = loan_service.create(loan_in)

    assert loan is not None
    assert loan.user_id == user.id
    assert loan.book_id == book.id
    assert hasattr(loan, "id")


def test_get_loan(db_session: Session, setup_user_and_book):
    """
    Teste la récupération d’un emprunt par ID.
    """
    user, book = setup_user_and_book
    loan_repo = LoanRepository(Loan, db_session)
    loan_service = LoanService(loan_repo)

    loan = loan_service.create(LoanCreate(user_id=user.id, book_id=book.id))
    retrieved_loan = loan_service.get(loan.id)

    assert retrieved_loan is not None
    assert retrieved_loan.id == loan.id
    assert retrieved_loan.user_id == user.id


def test_get_loans_by_user(db_session: Session, setup_user_and_book):
    """
    Teste la récupération de tous les emprunts d’un utilisateur.
    """
    user, book = setup_user_and_book
    loan_repo = LoanRepository(Loan, db_session)
    loan_service = LoanService(loan_repo)

    loan_service.create(LoanCreate(user_id=user.id, book_id=book.id))
    loan_service.create(LoanCreate(user_id=user.id, book_id=book.id))

    loans = loan_service.get_loans_by_user(user.id)

    assert len(loans) == 2
    for loan in loans:
        assert loan.user_id == user.id


def test_delete_loan(db_session: Session, setup_user_and_book):
    """
    Teste la suppression d’un emprunt.
    """
    user, book = setup_user_and_book
    loan_repo = LoanRepository(Loan, db_session)
    loan_service = LoanService(loan_repo)

    loan = loan_service.create(LoanCreate(user_id=user.id, book_id=book.id))
    loan_id = loan.id

    loan_service.remove(loan_id)
    assert loan_service.get(loan_id) is None
