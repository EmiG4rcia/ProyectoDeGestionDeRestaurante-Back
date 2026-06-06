from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean

from core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=True)
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=True)
    is_available = Column(Boolean, default=True)
    popularity_score = Column(Integer, default=0)