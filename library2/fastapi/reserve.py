from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from file import models, schemas
from fastapi import APIRouter

router = APIRouter()
@router.post("/create-reserve", response_model=schemas.ReservationOut)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(models.get_db)):
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get("/get-reserve", response_model=list[schemas.ReservationOut])
def get_reservations(db: Session = Depends(models.get_db)):
    return db.query(models.Reservation).all()

@router.put("/update-reserve{reservation_id}", response_model=schemas.ReservationOut)
def update_reservation(reservation_id: int, reservation: schemas.ReservationCreate, db: Session = Depends(
    models.get_db)):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.dict().items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.delete("/delete-reserve{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(models.get_db)):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return {"message": "Reservation deleted successfully"}

