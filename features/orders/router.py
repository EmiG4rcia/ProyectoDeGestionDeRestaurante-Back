from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

from fastapi import APIRouter, Depends, Query
from core.database import get_db
from core.dependencies import get_current_admin, get_sales_access
from features.orders.schemas import OrderResponse, OrderStatusUpdate, OrderCreate
from features.orders.service import get_orders, get_order_by_id, update_order_status
from features.orders.models import Order

router = APIRouter()


@router.get("", response_model=list[OrderResponse])
def list_orders(
    status: Optional[str] = Query(None),
    table_id: Optional[int] = Query(None),
    customer_id: Optional[int] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    skip: int = Query(0),
    limit: int = Query(50),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    orders = get_orders(
        db,
        order_status=status,
        table_id=table_id,
        customer_id=customer_id,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )

    result = []
    for order in orders:
        order_dict = {
            "id": order.id,
            "customer_id": order.customer_id,
            "table_id": order.table_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "customer_name": order.customer.name if order.customer else None,
            "table_number": order.table.table_number if order.table else None,
            "items": [
                {
                    "id": item.id,
                    "menu_item_id": item.menu_item_id,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "item_name": item.menu_item.name if item.menu_item else None,
                }
                for item in order.items
            ],
        }
        result.append(order_dict)
    return result


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    order = get_order_by_id(db, order_id)
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "table_id": order.table_id,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "customer_name": order.customer.name if order.customer else None,
        "table_number": order.table.table_number if order.table else None,
        "items": [
            {
                "id": item.id,
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "item_name": item.menu_item.name if item.menu_item else None,
            }
            for item in order.items
        ],
    }


@router.patch("/{order_id}/status", response_model=OrderResponse)
def change_order_status(
    order_id: int,
    body: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    order = update_order_status(db, order_id, body.status)
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "table_id": order.table_id,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "customer_name": order.customer.name if order.customer else None,
        "table_number": order.table.table_number if order.table else None,
        "items": [],
    }
    

@router.get("/summary")
def orders_summary(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    from datetime import date
    today = date.today()
    
    total_today = db.query(Order).filter(
        func.date(Order.created_at) == today
    ).count()
    
    pending = db.query(Order).filter(
        Order.status.in_(["pending", "confirmed", "preparing"])
    ).count()

    return {
        "orders_today": total_today,
        "pending_orders": pending,
    }
    
@router.post("")
def create_new_order(
    body: OrderCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    from features.orders.service import create_order
    order = create_order(db, body.customer_id, body.table_id, [i.model_dump() for i in body.items])
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "table_id": order.table_id,
        "status": order.status,
        "total_amount": order.total_amount,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "customer_name": None,
        "table_number": None,
        "items": [],
    }


@router.delete("/{order_id}")
def remove_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_sales_access),
):
    from features.orders.service import delete_order
    delete_order(db, order_id)
    return {"message": f"Pedido {order_id} eliminado correctamente"}    