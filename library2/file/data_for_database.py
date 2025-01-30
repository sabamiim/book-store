from sqlalchemy.orm import Session
from models import Book, User, Customer, Reservation, Author, Genre, Cities, AuthorBook, SessionLocal
from datetime import datetime
from decimal import Decimal


def insert_dummy_data(db: Session):
    genres = [Genre(name=f"Genre {i}") for i in range(1, 11)]
    db.add_all(genres)
    db.commit()

    books = [
        Book(title=f"Book {i}", isbn=f"97812345678{i}", price=100 + i, description=f"Description {i}", units=5,
             genre_id=i)
        for i in range(1, 11)
    ]
    db.add_all(books)
    db.commit()

    users = [
        User(username=f"user{i}", first_name=f"First{i}", last_name=f"Last{i}", email=f"user{i}@example.com",
             phone_number=f"+9812345678{i}", password_hash="hashed_password", user_role="customer")
        for i in range(1, 11)
    ]
    db.add_all(users)
    db.commit()

    # اضافه کردن مشتریان
    customers = [
        Customer(subscription_model="standard", user_id=i, wallet_money_amount=Decimal("1000.00"),
                 subscription_end_time=datetime.utcnow())
        for i in range(1, 11)
    ]
    db.add_all(customers)
    db.commit()

    reservations = [
        Reservation(subscription_model="standard", book_id=i, customer_id=i, price=Decimal("50.00"),
                    start_of_reservation=datetime.utcnow(), consideration=f"Reservation {i}")
        for i in range(1, 11)
    ]
    db.add_all(reservations)
    db.commit()

    cities = [Cities(name=f"City {i}") for i in range(1, 11)]
    db.add_all(cities)
    db.commit()

    authors = [
        Author(author_name=f"Author {i}", city_id=i, goodreads_link=f"http://goodreads.com/author{i}",
               bank_account_number=f"IR123456789{i}", user_id=i)
        for i in range(1, 11)
    ]
    db.add_all(authors)
    db.commit()

    author_books = [
        AuthorBook(author_id=i, book_id=i) for i in range(1, 11)
    ]
    db.add_all(author_books)
    db.commit()

db = SessionLocal()
insert_dummy_data(db)
db.close()
