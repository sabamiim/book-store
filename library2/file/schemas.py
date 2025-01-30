from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal




class BookBase(BaseModel):
    title: str
    isbn: str
    price: int
    description: str
    units: int
    genre_id: int

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    user_role: str

class UserCreate(UserBase):
    password_hash: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    subscription_model: str
    user_id: int
    wallet_money_amount: Decimal
    subscription_end_time: Optional[datetime] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int

    class Config:
        from_attributes = True


class ReservationBase(BaseModel):
    subscription_model: str
    book_id: int
    customer_id: int
    price: Decimal
    start_of_reservation: datetime
    consideration: str

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    id: int

    class Config:
        from_attributes = True

class AuthorBase(BaseModel):
    author_name: str
    city_id: Optional[int] = None
    goodreads_link: Optional[str] = None
    bank_account_number: Optional[str] = None
    user_id: Optional[int] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorOut(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreOut(GenreBase):
    id: int

    class Config:
        from_attributes = True

class CitiesBase(BaseModel):
    name: str

class CitiesCreate(CitiesBase):
    pass

class CitiesOut(CitiesBase):
    id: int

    class Config:
        from_attributes = True

class AuthorBookBase(BaseModel):
    author_id: int
    book_id: int

class AuthorBookCreate(AuthorBookBase):
    pass

class AuthorBookOut(AuthorBookBase):
    id: int

    class Config:
        from_attributes = True

