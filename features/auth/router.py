from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_admin
from features.auth.schemas import (
    LoginRequest,
    SalesVerifyRequest,
    ChangePasswordRequest,
    ChangeSalesPasswordRequest,
    RecoverPasswordRequest,
    TokenResponse,
    SalesTokenResponse,
)
from features.auth.service import (
    authenticate_admin,
    verify_sales_password,
    change_password,
    change_sales_password,
    recover_password,
)

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate_admin(db, request.username, request.password)
    return TokenResponse(access_token=token)


@router.post("/sales-verify", response_model=SalesTokenResponse)
def sales_verify(
    request: SalesVerifyRequest,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    admin_id = int(current_admin["admin_id"])
    sales_token = verify_sales_password(db, admin_id, request.password)
    return SalesTokenResponse(sales_token=sales_token)


@router.get("/me")
def get_me(current_admin: dict = Depends(get_current_admin)):
    return {"admin_id": current_admin["admin_id"]}


@router.patch("/change-password")
def update_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    change_password(
        db,
        int(current_admin["admin_id"]),
        request.current_password,
        request.new_password,
    )
    return {"message": "Contraseña actualizada correctamente"}


@router.patch("/change-sales-password")
def update_sales_password(
    request: ChangeSalesPasswordRequest,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    change_sales_password(
        db,
        int(current_admin["admin_id"]),
        request.current_password,
        request.new_sales_password,
    )
    return {"message": "Contraseña de ventas actualizada correctamente"}


@router.post("/recover")
def recover(request: RecoverPasswordRequest, db: Session = Depends(get_db)):
    recover_password(db, request.recovery_code, request.new_password)
    return {"message": "Contraseña recuperada correctamente"}