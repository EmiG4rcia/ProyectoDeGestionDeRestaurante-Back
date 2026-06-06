import secrets
import string
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import (
    verify_password,
    create_access_token,
    create_sales_token,
    get_password_hash,
)
from features.auth.models import AdminUser


def authenticate_admin(db: Session, username: str, password: str) -> str:
    admin = db.query(AdminUser).filter(AdminUser.username == username).first()

    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    admin.last_login = datetime.utcnow()
    db.commit()

    return create_access_token(data={"sub": str(admin.id)})


def verify_sales_password(db: Session, admin_id: int, password: str) -> str:
    admin = db.query(AdminUser).filter(AdminUser.id == admin_id).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin no encontrado",
        )

    if not verify_password(password, admin.sales_password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contraseña de ventas incorrecta",
        )

    return create_sales_token(data={"sub": str(admin.id)})


def change_password(
    db: Session,
    admin_id: int,
    current_password: str,
    new_password: str,
) -> None:
    admin = db.query(AdminUser).filter(AdminUser.id == admin_id).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin no encontrado",
        )

    if not verify_password(current_password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contraseña actual incorrecta",
        )

    admin.password_hash = get_password_hash(new_password)
    db.commit()


def change_sales_password(
    db: Session,
    admin_id: int,
    current_password: str,
    new_sales_password: str,
) -> None:
    admin = db.query(AdminUser).filter(AdminUser.id == admin_id).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin no encontrado",
        )

    if not verify_password(current_password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contraseña actual incorrecta",
        )

    admin.sales_password_hash = get_password_hash(new_sales_password)
    db.commit()


def recover_password(
    db: Session,
    recovery_code: str,
    new_password: str,
) -> None:
    admin = db.query(AdminUser).first()

    if not admin or not admin.recovery_code_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay código de recuperación configurado",
        )

    if not verify_password(recovery_code, admin.recovery_code_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Código de recuperación incorrecto",
        )

    admin.password_hash = get_password_hash(new_password)
    db.commit()


def generate_recovery_code() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(8))


def create_first_admin(
    db: Session,
    username: str,
    password: str,
    sales_password: str,
) -> tuple[AdminUser, str]:
    existing = db.query(AdminUser).filter(AdminUser.username == username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
        )

    recovery_code = generate_recovery_code()

    admin = AdminUser(
        username=username,
        password_hash=get_password_hash(password),
        sales_password_hash=get_password_hash(sales_password),
        recovery_code_hash=get_password_hash(recovery_code),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin, recovery_code