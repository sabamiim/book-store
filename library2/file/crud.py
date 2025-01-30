from datetime import datetime
from unicodedata import decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Session
from sqlalchemy.testing.suite.test_reflection import users

from database import *
from models import Book, Customer , Reservation


class BOOK_CRUD:

    def create_book(session: Session , title:str , isbn: int , price:int, description:str, units:int, author_id:int):
        new = Book(
            title = title ,
            isbn = isbn ,
            price = price,
            description = description,
            units = units,
            author_id = author_id
        )
        session.add(new)
        session.commit()
        session.refresh(new)
        return new

    def read_book(session: Session, title: str):
        read = Book(
            title=title,
            )
        session.read(read)
        session.commit()
        session.refresh(read)
        return read

    def update_book(session: Session, new_title: str, new_isbn: int, new_price: int, new_description: str,
                    new_units: int,new_author_id: int, id:int):
        update = session.query(Book).filter(Book.id == id).first()
        if update :

            update.title = new_title,
            update.isbn = new_isbn,
            update.price = new_price,
            update.description = new_description,
            update.units = new_units,
            update.author_id = new_author_id
        session.commit()
        session.refresh(update)
        return update

    def delete_book(session: Session, id: int):
        delete = session.query(Book).filter(Book.id == id).first()
        if delete:
            session.delete(delete)
            session.commit()
        return delete


class CRUD_USER:

    def create_user(session:Session , id : int , username : str , email : str , password_hash : str):
        new = users(
            id = id ,
            username = username,
            email = email,
            password_hash = password_hash
        )
        session.add(new)
        session.commit()
        session.refresh(new)
        return new

    def read_user(session: Session, username : str):
        read = users(
            username = username,
            )
        session.read(read)
        session.commit()
        session.refresh(read)
        return read

    def update_user(session: Session, username: str, id: int, email: str, password_hash: str):

        user_to_update = session.query(users).filter(users.id == id).first()

        if user_to_update:

            user_to_update.username = username
            user_to_update.email = email
            user_to_update.password_hash = password_hash

            session.commit()
            session.refresh(user_to_update)

            return user_to_update
        else:
            return None

    def delete_user(session: Session, username: str, id: int, email: str, password_hash: str):

        delete_user = session.query(users).filter(users.id == id).first()

        if delete_user:

            delete_user.username = username
            delete_user.email = email
            delete_user.password_hash = password_hash

            session.commit()
            session.refresh(delete_user)

            return delete_user

class CUSTOMER_CRUD:
    def create_customer(session: Session, id: int, subscription_model: str, user_id: int,
                        wallet_money_amount: decimal, subscription_end_time: datetime):
        new = Customer(
            id=id,
            subscription_model=subscription_model,
            user_id=user_id,
            wallet_money_amount=wallet_money_amount,
            subscription_end_time=subscription_end_time
        )
        session.add(new)
        session.commit()
        session.refresh(new)
        return new

    def read_customer(session: Session, id: int):
        read = session.query(Customer).filter(Customer.id == id).first()
        if not read:
            return None
        return read

    def update_customer(session: Session, id: int, subscription_model: str, user_id: int,
                        wallet_money_amount: decimal, subscription_end_time: datetime):
        update = session.query(Customer).filter(Customer.id == id).first()
        if update:
            update.subscription_model = subscription_model
            update.user_id = user_id
            update.wallet_money_amount = wallet_money_amount
            update.subscription_end_time = subscription_end_time
            session.commit()
            session.refresh(update)
        return update

    def delete_customer(session: Session, id: int):
        delete = session.query(Customer).filter(Customer.id == id).first()
        if delete:
            session.delete(delete)
            session.commit()
        return delete


class RESERVATION_CRUD:
    def reservation_create(session: Session, id: int, subscription_model: str, book_id: int, customer_id: str,
                           price: decimal, start_of_reservation: datetime, consideration: str):
        new = Reservation(
            id=id,
            subscription_model=subscription_model,
            book_id=book_id,
            customer_id=customer_id,
            price=price,
            start_of_reservation=start_of_reservation,
            consideration=consideration
        )
        session.add(new)
        session.commit()
        session.refresh(new)
        return new

    def read_reservation(session: Session, id: int):
        read = session.query(Reservation).filter(Reservation.id == id).first()
        if not read:
            return None
        return read

    def update_reservation(session: Session, id: int, subscription_model: str, book_id: int, customer_id: str,
                           price: decimal, start_of_reservation: datetime, consideration: str):
        update = session.query(Reservation).filter(Reservation.id == id).first()
        if update:
            update.subscription_model = subscription_model
            update.book_id = book_id
            update.customer_id = customer_id
            update.price = price
            update.start_of_reservation = start_of_reservation
            update.consideration = consideration
            session.commit()
            session.refresh(update)
        return update

    def delete_reservation(session: Session, id: int):
        delete = session.query(Reservation).filter(Reservation.id == id).first()
        if delete:
            session.delete(delete)
            session.commit()
        return delete
