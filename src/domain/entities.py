from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """
    Entidad que representa un producto (zapato) en el e-commerce.

    Contiene los datos del producto y las reglas de negocio
    relacionadas con inventario y disponibilidad.

    Atributos:
        id: Identificador único del producto (None si aún no está guardado).
        name: Nombre del producto.
        brand: Marca del producto (Nike, Adidas, Puma, etc.).
        category: Categoría del producto (Running, Casual, Formal).
        size: Talla del producto.
        color: Color del producto.
        price: Precio del producto (debe ser mayor a 0).
        stock: Cantidad disponible en inventario (no puede ser negativo).
        description: Descripción del producto.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Valida los datos del producto al momento de crearlo.

        Raises:
            ValueError: Si el precio es menor o igual a 0.
            ValueError: Si el stock es negativo.
            ValueError: Si el nombre está vacío.
        """
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

    def is_available(self) -> bool:
        """
        Verifica si el producto tiene stock disponible para la venta.

        Returns:
            True si el stock es mayor a 0, False en caso contrario.
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto al realizar una venta.

        Args:
            quantity: Cantidad a reducir del stock.

        Raises:
            ValueError: Si la cantidad no es positiva.
            ValueError: Si no hay suficiente stock disponible.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a 0.")
        if quantity > self.stock:
            raise ValueError(
                f"Stock insuficiente. Stock actual: {self.stock}, "
                f"cantidad solicitada: {quantity}."
            )
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto al recibir nueva mercancía.

        Args:
            quantity: Cantidad a agregar al stock.

        Raises:
            ValueError: Si la cantidad no es positiva.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a agregar debe ser mayor a 0.")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en la conversación del chat.

    Cada mensaje pertenece a una sesión de usuario y tiene
    un rol que indica si lo envió el usuario o el asistente de IA.

    Atributos:
        id: Identificador único del mensaje (None si no está guardado).
        session_id: Identificador de la sesión del usuario.
        role: Rol del emisor del mensaje ('user' o 'assistant').
        message: Contenido del mensaje.
        timestamp: Fecha y hora en que se creó el mensaje.
    """
    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Valida los datos del mensaje al momento de crearlo.

        Raises:
            ValueError: Si el rol no es 'user' o 'assistant'.
            ValueError: Si el mensaje está vacío.
            ValueError: Si el session_id está vacío.
        """
        if self.role not in ('user', 'assistant'):
            raise ValueError(
                f"El rol debe ser 'user' o 'assistant'. "
                f"Se recibió: '{self.role}'."
            )
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío.")
        if not self.session_id or not self.session_id.strip():
            raise ValueError("El session_id no puede estar vacío.")

    def is_from_user(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el usuario.

        Returns:
            True si el rol es 'user', False en caso contrario.
        """
        return self.role == 'user'

    def is_from_assistant(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el asistente de IA.

        Returns:
            True si el rol es 'assistant', False en caso contrario.
        """
        return self.role == 'assistant'


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.

    Mantiene los mensajes recientes para que la IA tenga
    memoria de la conversación y pueda dar respuestas coherentes.

    Atributos:
        messages: Lista completa de mensajes de la sesión.
        max_messages: Número máximo de mensajes recientes a considerar.
    """
    messages: list[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> list[ChatMessage]:
        """
        Retorna los últimos N mensajes de la conversación.

        Returns:
            Lista con los últimos max_messages mensajes,
            en orden cronológico (más antiguos primero).
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea el historial de mensajes para incluirlo en el prompt de IA.

        Convierte los mensajes recientes en un string legible que
        Google Gemini puede usar como contexto conversacional.

        Returns:
            String con el historial formateado. Ejemplo:
            'Usuario: busco zapatos para correr\\nAsistente: tengo varias opciones...'
        """
        lines = []
        for msg in self.get_recent_messages():
            if msg.is_from_user():
                lines.append(f"Usuario: {msg.message}")
            else:
                lines.append(f"Asistente: {msg.message}")
        return "\n".join(lines)