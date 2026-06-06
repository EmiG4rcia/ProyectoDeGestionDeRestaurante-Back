from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_admin
from features.tables.schemas import TableCreate, TableUpdate, TableResponse
from features.tables.service import (
    get_tables,
    get_table_by_id,
    create_table,
    update_table,
    delete_table,
    generate_qr_base64,
)

router = APIRouter()


@router.get("", response_model=list[TableResponse])
def list_tables(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return get_tables(db)


@router.post("", response_model=TableResponse)
def create_new_table(
    data: TableCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return create_table(db, data)


@router.put("/{table_id}", response_model=TableResponse)
def update_existing_table(
    table_id: int,
    data: TableUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return update_table(db, table_id, data)


@router.delete("/{table_id}")
def delete_existing_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    delete_table(db, table_id)
    return {"message": f"Mesa {table_id} eliminada correctamente"}


@router.get("/{table_id}/qr")
def get_table_qr(
    table_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    table = get_table_by_id(db, table_id)
    qr_base64 = generate_qr_base64(table)
    return {
        "table_id": table.id,
        "table_number": table.table_number,
        "qr_token": table.qr_token,
        "qr_image_base64": qr_base64,
        "whatsapp_url": f"https://wa.me/14155238886?text={table.qr_token}",
    }