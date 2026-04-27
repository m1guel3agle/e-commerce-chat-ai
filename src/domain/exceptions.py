"""
Excepciones específicas del dominio de e-commerce.

Representan errores de negocio, no errores técnicos.
Se usan para comunicar situaciones inválidas de forma
clara y descriptiva entre las capas de la aplicación.
"""


class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe en el repositorio.

    Ejemplo de uso:
        raise ProductNotFoundError(product_id=5)
        # Mensaje: "Producto con ID 5 no encontrado"
    """

    def __init__(self, product_id: int = None):
        """
        Args:
            product_id: ID del producto que no se encontró.
                        Si no se pasa, usa un mensaje genérico.
        """
        if product_id is not None:
            self.message = f"Producto con ID {product_id} no encontrado."
        else:
            self.message = "Producto no encontrado."
        super().__init__(self.message)


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.

    Ejemplo de uso:
        raise InvalidProductDataError("El precio no puede ser negativo")
    """

    def __init__(self, message: str = "Datos de producto inválidos."):
        """
        Args:
            message: Descripción del error de validación.
        """
        self.message = message
        super().__init__(self.message)


class ChatServiceError(Exception):
    """
    Se lanza cuando ocurre un error en el servicio de chat.

    Por ejemplo, si la IA no responde o el historial
    no se puede recuperar correctamente.

    Ejemplo de uso:
        raise ChatServiceError("No se pudo conectar con Gemini AI")
    """

    def __init__(self, message: str = "Error en el servicio de chat."):
        """
        Args:
            message: Descripción del error ocurrido en el chat.
        """
        self.message = message
        super().__init__(self.message)