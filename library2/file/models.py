import re
from datetime import datetime

from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Index
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://saba:saba4055@localhost/library"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    units = Column(Integer, nullable=False)
    genre_id = Column(Integer, ForeignKey('genre.id'), nullable=False)
    genre = relationship("Genre", back_populates="books")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    user_role = Column(String, nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("ایمیل وارد شده معتبر نیست.")
        return email

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        phone_regex = r'^\+98\d{10}$'
        if not re.match(phone_regex, phone_number):
            raise ValueError("شماره تلفن وارد شده معتبر نیست. شماره باید با +98 شروع شده و شامل 10 رقم باشد.")
        return phone_number


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    subscription_model = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    wallet_money_amount = Column(Numeric(10, 2), default=0.00)
    subscription_end_time = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="customers")


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, index=True)
    subscription_model = Column(String, nullable=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    price = Column(Numeric(10, 2), default=0.00)
    start_of_reservation = Column(DateTime, nullable=True)
    consideration = Column(String, nullable=True)
    book = relationship("Book", back_populates="reservations")
    customer = relationship("Customer", back_populates="reservations")


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    goodreads_link = Column(String, unique=True, index=True, nullable=True)
    bank_account_number = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="authors")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="genre")


class Cities(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class AuthorBook(Base):
    __tablename__ = "authorbook"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    author = relationship("Author", back_populates="books")
    book = relationship("Book", back_populates="authors")

class ReservationQueue(Base):
    __tablename__ = "reservation_queue"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    book = relationship("Book")