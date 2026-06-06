from typing import Optional, List
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from features.orders.models import Order, OrderItem
from features.customers.models import Customer
from features.tables.models import Table
from features.menu.models import MenuItem


VALID_STATUSES = [
    "pending", "confirmed", "preparing",
    "ready", "delivered", "cancelled"
]


def get_orders(
    db: Session,
    order_status: Optional[str] = None,
    table_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Order]:
    query = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.menu_item),
        joinedload(Order.customer),
        joinedload(Order.table),
    )

    if order_status:
        query = query.filter(Order.status == order_status)
    if table_id:
        query = query.filter(Order.table_id == table_id)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    if date_from:
        query = query.filter(Order.created_at >= date_from)
    if date_to:
        query = query.filter(Order.created_at <= date_to)

    return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()


def get_order_by_id(db: Session, order_id: int) -> Order:
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.menu_item),
        joinedload(Order.customer),
        joinedload(Order.table),
    ).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {order_id} no encontrado",
        )
    return order


def update_order_status(db: Session, order_id: int, new_status: str) -> Order:
    if new_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado inválido. Valores permitidos: {VALID_STATUSES}",
        )

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {order_id} no encontrado",
        )

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order

def create_order(
    db: Session,
    customer_id: Optional[int],
    table_id: Optional[int],
    items: list,
) -> Order:
    total = sum(item["unit_price"] * item["quantity"] for item in items)

    order = Order(
        customer_id=customer_id,
        table_id=table_id,
        status="confirmed",
        total_amount=total,
    )
    db.add(order)
    db.flush()

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item["menu_item_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int) -> None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {order_id} no encontrado",
        )
    db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
    db.delete(order)
    db.commit()