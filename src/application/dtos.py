from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos entre capas.

    Pydantic valida automáticamente los tipos y ejecuta
    los validadores personalizados al crear la instancia.

    Atributos:
        id: Identificador del producto (opcional al crear uno nuevo).
        name: Nombre del producto.
        brand: Marca del producto.
        category: Categoría del producto.
        size: Talla del producto.
        color: Color del producto.
        price: Precio (debe ser mayor a 0).
        stock: Stock disponible (no puede ser negativo).
        description: Descripción del producto.
    """
    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @validator('price')
    def price_must_be_positive(cls, v):
        """Valida que el precio sea mayor a 0."""
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        return v

    @validator('stock')
    def stock_must_be_non_negative(cls, v):
        """Valida que el stock no sea negativo."""
        if v < 0:
            raise ValueError("El stock no puede ser negativo.")
        return v

    class Config:
        from_attributes = True


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir el mensaje del usuario en el endpoint de chat.

    Atributos:
        session_id: Identificador único de la sesión del usuario.
        message: Contenido del mensaje enviado por el usuario.
    """
    session_id: str
    message: str

    @validator('message')
    def message_not_empty(cls, v):
        """Valida que el mensaje no esté vacío."""
        if not v or not v.strip():
            raise ValueError("El mensaje no puede estar vacío.")
        return v

    @validator('session_id')
    def session_id_not_empty(cls, v):
        """Valida que el session_id no esté vacío."""
        if not v or not v.strip():
            raise ValueError("El session_id no puede estar vacío.")
        return v


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para retornar la respuesta del chat al cliente.

    Contiene tanto el mensaje del usuario como la respuesta
    generada por la IA en un mismo objeto.

    Atributos:
        session_id: Identificador de la sesión.
        user_message: Mensaje original del usuario.
        assistant_message: Respuesta generada por la IA.
        timestamp: Momento en que se procesó el mensaje.
    """
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """
    DTO para mostrar un mensaje del historial de conversación.

    Atributos:
        id: Identificador del mensaje.
        role: Rol del emisor ('user' o 'assistant').
        message: Contenido del mensaje.
        timestamp: Momento en que se envió el mensaje.
    """
    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True