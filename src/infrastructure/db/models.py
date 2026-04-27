from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Index
from src.infrastructure.db.database import Base


class ProductModel(Base):
    """
    Modelo ORM que representa la tabla 'products' en la base de datos.

    Cada instancia corresponde a un zapato en el inventario.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100))
    category = Column(String(100))
    size = Column(String(20))
    color = Column(String(50))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(Text)

    __table_args__ = (
        Index('ix_products_brand', 'brand'),
        Index('ix_products_category', 'category'),
    )


class ChatMemoryModel(Base):
    """
    Modelo ORM que representa la tabla 'chat_memory' en la base de datos.

    Almacena el historial de conversaciones del chat con IA.
    """
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)