from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LoanBase(BaseModel):
    user_id: int = Field(..., description="ID de l'utilisateur")
    book_id: int = Field(..., description="ID du livre")
    return_date: Optional[datetime] = Field(None, description="Date de retour prévue")
    returned: bool = Field(False, description="Indique si le livre a été retourné")


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    return_date: Optional[datetime] = Field(None, description="Nouvelle date de retour")
    returned: Optional[bool] = Field(None, description="Statut de retour du livre")


class LoanInDBBase(LoanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Loan(LoanInDBBase):
    pass
