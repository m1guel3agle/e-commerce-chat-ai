import sys
sys.path.insert(0, '.')
from src.domain.entities import Product, ChatMessage, ChatContext
from datetime import datetime

# --- Prueba Product ---
p = Product(id=1, name="Air Zoom", brand="Nike", category="Running",
            size="42", color="Negro", price=120.0, stock=5, description="Zapato running")
print("Disponible:", p.is_available())       # True
p.reduce_stock(2)
print("Stock tras vender 2:", p.stock)       # 3
p.increase_stock(10)
print("Stock tras recibir 10:", p.stock)     # 13

# --- Prueba validaciones ---
try:
    Product(id=None, name="X", brand="Y", category="Z",
            size="40", color="Rojo", price=-10, stock=0, description="")
except ValueError as e:
    print("Error esperado:", e)

try:
    Product(id=None, name="X", brand="Y", category="Z",
            size="40", color="Rojo", price=50, stock=-5, description="")
except ValueError as e:
    print("Error esperado:", e)

# --- Prueba ChatMessage ---
m1 = ChatMessage(id=1, session_id="s1", role="user",
                 message="Busco zapatos Nike", timestamp=datetime.now())
m2 = ChatMessage(id=2, session_id="s1", role="assistant",
                 message="Tengo varias opciones", timestamp=datetime.now())
print("Es del usuario:", m1.is_from_user())       # True
print("Es del asistente:", m1.is_from_assistant()) # False

# --- Prueba ChatContext ---
ctx = ChatContext(messages=[m1, m2])
print("\nHistorial formateado:")
print(ctx.format_for_prompt())

from src.domain.repositories import IProductRepository, IChatRepository

# Verificar que son abstractas (no se pueden instanciar)
try:
    IProductRepository()
except TypeError as e:
    print("Correcto, es abstracta:", e)

try:
    IChatRepository()
except TypeError as e:
    print("Correcto, es abstracta:", e)

    from src.domain.exceptions import (
    ProductNotFoundError,
    InvalidProductDataError,
    ChatServiceError
)

# Con ID
try:
    raise ProductNotFoundError(product_id=42)
except ProductNotFoundError as e:
    print(e)  # Producto con ID 42 no encontrado.

# Sin ID
try:
    raise ProductNotFoundError()
except ProductNotFoundError as e:
    print(e)  # Producto no encontrado.

# Datos inválidos
try:
    raise InvalidProductDataError("El precio no puede ser negativo.")
except InvalidProductDataError as e:
    print(e)  # El precio no puede ser negativo.

# Error de chat
try:
    raise ChatServiceError("No se pudo conectar con Gemini AI.")
except ChatServiceError as e:
    print(e)  # No se pudo conectar con Gemini AI.