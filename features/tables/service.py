import secrets
import qrcode
import io
import base64
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from features.tables.models import Table
from features.tables.schemas import TableCreate, TableUpdate


def get_tables(db: Session) -> List[Table]:
    return db.query(Table).order_by(Table.table_number).all()


def get_table_by_id(db: Session, table_id: int) -> Table:
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mesa {table_id} no encontrada",
        )
    return table


def create_table(db: Session, data: TableCreate) -> Table:
    existing = db.query(Table).filter(
        Table.table_number == data.table_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una mesa con el número {data.table_number}",
        )

    qr_token = f"table_{data.table_number}_{secrets.token_hex(4)}"

    table = Table(
        table_number=data.table_number,
        qr_token=qr_token,
        status="available",
    )
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


def update_table(db: Session, table_id: int, data: TableUpdate) -> Table:
    table = get_table_by_id(db, table_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(table, key, value)
    db.commit()
    db.refresh(table)
    return table


def delete_table(db: Session, table_id: int) -> None:
    table = get_table_by_id(db, table_id)
    db.delete(table)
    db.commit()


def generate_qr_base64(table: Table) -> str:
    whatsapp_number = "14155238886"
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={table.qr_token}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(whatsapp_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")