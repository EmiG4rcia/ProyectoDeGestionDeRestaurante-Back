from decimal import Decimal
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from features.sales.models import Payment
from features.orders.models import Order
from features.orders.models import Order

VALID_PAYMENT_STATUSES = ["pending", "payment_received", "completed", "failed"]


def get_payments(
    db: Session,
    payment_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Payment]:
    query = db.query(Payment).options(
        joinedload(Payment.order)
    )
    if payment_status:
        query = query.filter(Payment.status == payment_status)

    return query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()


def get_sales_summary(db: Session) -> dict:
    total_orders = db.query(Order).count()

    completed = db.query(Payment).filter(
        Payment.status == "completed"
    ).all()
    total_revenue = sum(p.amount or 0 for p in completed)

    pending_payments = db.query(Payment).filter(
        Payment.status == "pending"
    ).count()

    completed_payments = db.query(Payment).filter(
        Payment.status == "completed"
    ).count()

    payment_received = db.query(Payment).filter(
        Payment.status == "payment_received"
    ).count()

    return {
        "total_orders": total_orders,
        "total_revenue": Decimal(str(total_revenue)),
        "pending_payments": pending_payments,
        "completed_payments": completed_payments,
        "payment_received_pending": payment_received,
    }


def update_payment_status(
    db: Session,
    payment_id: int,
    new_status: str,
) -> Payment:
    if new_status not in VALID_PAYMENT_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado inválido. Valores permitidos: {VALID_PAYMENT_STATUSES}",
        )

    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pago {payment_id} no encontrado",
        )

    payment.status = new_status
    db.commit()
    db.refresh(payment)
    return payment

def create_payment(
    db: Session,
    order_id: int,
    amount: float,
    method: str,
) -> Payment:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {order_id} no encontrado",
        )

    existing = db.query(Payment).filter(Payment.order_id == order_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este pedido ya tiene un pago registrado",
        )

    payment = Payment(
        order_id=order_id,
        amount=amount,
        method=method,
        status="completed",
    )
    db.add(payment)

    order.status = "delivered"
    db.commit()
    db.refresh(payment)
    return payment