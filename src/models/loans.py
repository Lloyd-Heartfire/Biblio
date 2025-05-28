from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Loan(Base):
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    returned = Column(Date, nullable=True)

    # Relations
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")
