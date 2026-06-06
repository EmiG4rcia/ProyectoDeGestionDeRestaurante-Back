from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_admin
from features.menu.schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from features.menu.service import (
    get_menu_items,
    get_menu_item_by_id,
    create_menu_item,
    update_menu_item,
    delete_menu_item,
    toggle_availability,
)

router = APIRouter()


@router.get("", response_model=list[MenuItemResponse])
def list_menu_items(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return get_menu_items(db)


@router.post("", response_model=MenuItemResponse)
def create_item(
    data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return create_menu_item(db, data)


@router.put("/{item_id}", response_model=MenuItemResponse)
def update_item(
    item_id: int,
    data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return update_menu_item(db, item_id, data)


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    delete_menu_item(db, item_id)
    return {"message": f"Item {item_id} eliminado correctamente"}


@router.patch("/{item_id}/availability", response_model=MenuItemResponse)
def toggle_item_availability(
    item_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return toggle_availability(db, item_id)