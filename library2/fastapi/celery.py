from file.main import celery_app
from file.models import get_db
from file.models import ReservationQueue, Book, Reservation, User


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