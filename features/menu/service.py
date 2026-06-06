from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from features.menu.models import MenuItem
from features.menu.schemas import MenuItemCreate, MenuItemUpdate


def get_menu_items(db: Session) -> List[MenuItem]:
    return db.query(MenuItem).order_by(MenuItem.category, MenuItem.name).all()


def get_menu_item_by_id(db: Session, item_id: int) -> MenuItem:
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} no encontrado",
        )
    return item


def create_menu_item(db: Session, data: MenuItemCreate) -> MenuItem:
    item = MenuItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_menu_item(db: Session, item_id: int, data: MenuItemUpdate) -> MenuItem:
    item = get_menu_item_by_id(db, item_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, item_id: int) -> None:
    item = get_menu_item_by_id(db, item_id)
    db.delete(item)
    db.commit()


def toggle_availability(db: Session, item_id: int) -> MenuItem:
    item = get_menu_item_by_id(db, item_id)
    item.is_available = not item.is_available
    db.commit()
    db.refresh(item)
    return item