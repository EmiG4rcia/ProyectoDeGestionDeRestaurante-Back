from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_admin, get_sales_access
from features.customers.schemas import CustomerCreate, CustomerUpdate
from features.customers.service import (
    get_customers,
    get_customer_by_id,
    get_customer_order_count,
    create_customer,
    update_customer,
    delete_customer,
)
from features.orders.models import Order

router = APIRouter()


@router.get("")
def list_customers(
    skip: int = Query(0),
    limit: int = Query(50),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    customers = get_customers(db, skip=skip, limit=limit)
    return [
        {
            "id": c.id,
            "phone_number": c.phone_number,
            "name": c.name,
            "created_at": c.created_at,
            "total_orders": get_customer_order_count(db, c.id),
        }
        for c in customers
    ]


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    customer = get_customer_by_id(db, customer_id)
    orders = db.query(Order).filter(
        Order.customer_id == customer_id
    ).order_by(Order.created_at.desc()).all()

    return {
        "id": customer.id,
        "phone_number": customer.phone_number,
        "name": customer.name,
        "created_at": customer.created_at,
        "orders": [
            {
                "id": o.id,
                "status": o.status,
                "total_amount": o.total_amount,
                "created_at": o.created_at,
            }
            for o in orders
        ],
    }


@router.post("")
def create_new_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    customer = create_customer(db, data)
    return {
        "id": customer.id,
        "phone_number": customer.phone_number,
        "name": customer.name,
        "created_at": customer.created_at,
        "total_orders": 0,
    }


@router.patch("/{customer_id}")
def edit_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    customer = update_customer(db, customer_id, data)
    return {
        "id": customer.id,
        "phone_number": customer.phone_number,
        "name": customer.name,
        "created_at": customer.created_at,
        "total_orders": get_customer_order_count(db, customer.id),
    }


@router.delete("/{customer_id}")
def remove_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    delete_customer(db, customer_id)
    return {"message": f"Cliente {customer_id} eliminado correctamente"}