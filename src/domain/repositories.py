from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.

    Las implementaciones concretas estarán en la capa de
    infraestructura. El dominio solo conoce esta interfaz,
    no sabe si los datos vienen de SQLite, PostgreSQL, etc.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos del repositorio.

        Returns:
            Lista con todos los productos disponibles.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su identificador único.

        Args:
            product_id: ID del producto a buscar.

        Returns:
            El producto si existe, None si no se encuentra.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.

        Args:
            brand: Nombre de la marca (Nike, Adidas, Puma, etc.).

        Returns:
            Lista de productos que pertenecen a esa marca.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene todos los productos de una categoría específica.

        Args:
            category: Nombre de la categoría (Running, Casual, Formal).

        Returns:
            Lista de productos que pertenecen a esa categoría.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en el repositorio.

        Si el producto tiene ID, lo actualiza.
        Si no tiene ID, crea uno nuevo y le asigna ID.

        Args:
            product: Producto a guardar o actualizar.

        Returns:
            El producto guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id: ID del producto a eliminar.

        Returns:
            True si se eliminó correctamente, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interface que define el contrato para gestionar
    el historial de conversaciones del chat.

    Permite guardar y recuperar mensajes para mantener
    la memoria conversacional entre turnos.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial de conversación.

        Args:
            message: Mensaje a guardar.

        Returns:
            El mensaje guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión.

        Args:
            session_id: Identificador de la sesión del usuario.
            limit: Si se define, retorna solo los últimos N mensajes.

        Returns:
            Lista de mensajes en orden cronológico (más antiguos primero).
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Args:
            session_id: Identificador de la sesión a eliminar.

        Returns:
            Cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(
        self, session_id: str, count: int
    ) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión.

        Crucial para construir el ChatContext que se envía
        a la IA como memoria conversacional.

        Args:
            session_id: Identificador de la sesión.
            count: Número de mensajes recientes a obtener.

        Returns:
            Lista de mensajes en orden cronológico (más antiguos primero).
        """
        pass