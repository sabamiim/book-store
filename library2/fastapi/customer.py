from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from file import models, schemas

router = APIRouter()

@router.post("/create-customer", response_model=schemas.CustomerOut)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(models.get_db)):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/get-customer", response_model=list[schemas.CustomerOut])
def get_customers(db: Session = Depends(models.get_db)):
    return db.query(models.Customer).all()

@router.put("/update-customer{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(models.get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/delete-customer{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(models.get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}