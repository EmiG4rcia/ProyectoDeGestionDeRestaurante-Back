from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_admin, get_sales_access
from features.sales.schemas import PaymentStatusUpdate, SalesSummary, PaymentCreate
from features.sales.service import (
    get_payments,
    get_sales_summary,
    update_payment_status,
    create_payment,
)

router = APIRouter()


@router.get("/summary", response_model=SalesSummary)
def sales_summary(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    return get_sales_summary(db)


@router.get("/payments")
def list_payments(
    status: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(50),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    payments = get_payments(db, payment_status=status, skip=skip, limit=limit)
    result = []
    for payment in payments:
        result.append({
            "id": payment.id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "method": payment.method,
            "status": payment.status,
            "created_at": payment.created_at,
            "customer_name": payment.order.customer.name if payment.order and payment.order.customer else None,
            "table_number": payment.order.table.table_number if payment.order and payment.order.table else None,
        })
    return result


@router.patch("/payments/{payment_id}")
def change_payment_status(
    payment_id: int,
    body: PaymentStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    payment = update_payment_status(db, payment_id, body.status)
    return {
        "id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "method": payment.method,
        "status": payment.status,
        "created_at": payment.created_at,
    }
    

@router.post("/payments")
def register_payment(
    body: PaymentCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    payment = create_payment(db, body.order_id, body.amount, body.method)
    return {
        "id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "method": payment.method,
        "status": payment.status,
        "created_at": payment.created_at,
    }