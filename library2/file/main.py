from celery import Celery
from models import get_db
from models import ReservationQueue, User
from pydantic import BaseModel
from fastapi import  HTTPException, FastAPI
from sqlalchemy.orm import Session
from models import Reservation, Book



app = FastAPI()


SECRET_KEY = "8de4f599e8a9f04d9ae3885527b064aec64ce726730b7aaf546769bbc65fbd3a"
ALGORITHM = "HS256"


users_db = {}



class User(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str




books_db = {
    1: {"title": "Book 1", "units_available": 3},
    2: {"title": "Book 2", "units_available": 0}
}

reservations_db = []


@app.post("/reserve")
async def reserve(user_email: str, book_id: int):
    user = users_db.get(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = books_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book['units_available'] > 0:
        if user['wallet_balance'] < 1000:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        book['units_available'] -= 1
        user['wallet_balance'] -= 1000
        reservations_db.append({"user": user_email, "book_id": book_id, "status": "Reserved"})
        return {"message": "Reservation successful", "book_title": book['title']}

    reservations_db.append({"user": user_email, "book_id": book_id, "status": "Scheduled"})
    return {"message": "Book added to queue", "book_title": book['title']}





celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "tasks.process_reservation_queue": {"queue": "reservations"},
}


def instant_reserve(db: Session, user_id: int, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.reserved_units >= book.total_units:
        raise HTTPException(status_code=400, detail="No available units for reservation")

    new_reservation = Reservation(user_id=user_id, book_id=book_id)

    book.reserved_units += 1
    db.add(new_reservation)
    db.commit()

    return {"message": "Book reserved successfully"}
def add_to_reservation_queue(db: Session, user_id: int, book_id: int):
    queue_entry = ReservationQueue(user_id=user_id, book_id=book_id)
    db.add(queue_entry)
    db.commit()

    return {"message": "Added to reservation queue"}





@celery_app.task
def process_reservation_queue(book_id: int):
    db = next(get_db())

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.reserved_units >= book.total_units:
        return "No available units"

    queue_entries = db.query(ReservationQueue).filter(ReservationQueue.book_id == book_id).order_by(
        ReservationQueue.user.has(User.is_premium.desc()),
        ReservationQueue.created_at.asc()
    ).all()

    for entry in queue_entries:
        user = db.query(User).filter(User.id == entry.user_id).first()

        if user.wallet_balance < book.price:
            db.delete(entry)
            db.commit()
            continue

        new_reservation = Reservation(user_id=entry.user_id, book_id=book_id)
        book.reserved_units += 1
        user.wallet_balance -= book.price

        db.add(new_reservation)
        db.delete(entry)
        db.commit()

        return f"Reserved for user {entry.user_id}"

    return "No users available for reservation"
