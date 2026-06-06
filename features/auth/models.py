from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func

from core.database import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    sales_password_hash = Column(String(255), nullable=False)
    recovery_code_hash = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    last_login = Column(TIMESTAMP, nullable=True)