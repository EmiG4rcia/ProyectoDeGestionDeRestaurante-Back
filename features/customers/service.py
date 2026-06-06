from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from features.customers.models import Customer
from features.customers.schemas import CustomerCreate, CustomerUpdate
from features.orders.models import Order


def get_customers(db: Session, skip: int = 0, limit: int = 50) -> List[Customer]:
    return db.query(Customer).order_by(Customer.created_at.desc()).offset(skip).limit(limit).all()


def get_customer_by_id(db: Session, customer_id: int) -> Customer:
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente {customer_id} no encontrado",
        )
    return customer


def get_customer_order_count(db: Session, customer_id: int) -> int:
    return db.query(Order).filter(Order.customer_id == customer_id).count()


def create_customer(db: Session, data: CustomerCreate) -> Customer:
    existing = db.query(Customer).filter(
        Customer.phone_number == data.phone_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con ese número de teléfono",
        )
    customer = Customer(
        phone_number=data.phone_number,
        name=data.name,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer_id: int, data: CustomerUpdate) -> Customer:
    customer = get_customer_by_id(db, customer_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int) -> None:
    customer = get_customer_by_id(db, customer_id)
    db.delete(customer)
    db.commit()