import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import ProductDTO, ChatMessageRequestDTO
from src.domain.entities import Product, ChatMessage
from src.domain.exceptions import ProductNotFoundError, ChatServiceError


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────

def make_product(**kwargs):
    """Crea un producto de prueba con valores por defecto."""
    defaults = dict(
        id=1, name="Air Zoom", brand="Nike", category="Running",
        size="42", color="Negro", price=120.0, stock=5,
        description="Zapato running"
    )
    defaults.update(kwargs)
    return Product(**defaults)


# ─────────────────────────────────────────────
# Tests ProductService
# ─────────────────────────────────────────────

class TestProductService:
    """Tests para el servicio de productos."""

    @pytest.fixture
    def service(self, mock_product_repository):
        """Instancia de ProductService con repositorio mockeado."""
        return ProductService(repository=mock_product_repository)

    def test_get_all_products(self, service, mock_product_repository):
        """Verifica que retorna todos los productos como DTOs."""
        mock_product_repository.get_all.return_value = [make_product()]
        result = service.get_all_products()
        assert len(result) == 1
        assert result[0].name == "Air Zoom"

    def test_get_all_products_lista_vacia(self, service, mock_product_repository):
        """Verifica que retorna lista vacía si no hay productos."""
        mock_product_repository.get_all.return_value = []
        result = service.get_all_products()
        assert result == []

    def test_get_product_by_id_existente(self, service, mock_product_repository):
        """Verifica que retorna el producto correcto si existe."""
        mock_product_repository.get_by_id.return_value = make_product(id=1)
        result = service.get_product_by_id(1)
        assert result.id == 1
        assert result.brand == "Nike"

    def test_get_product_by_id_no_existente(self, service, mock_product_repository):
        """Verifica que lanza ProductNotFoundError si no existe."""
        mock_product_repository.get_by_id.return_value = None
        with pytest.raises(ProductNotFoundError):
            service.get_product_by_id(999)

    def test_get_available_products_con_stock(self, service, mock_product_repository):
        """Verifica que solo retorna productos con stock > 0."""
        mock_product_repository.get_all.return_value = [
            make_product(id=1, stock=5),
            make_product(id=2, stock=0),
        ]
        result = service.get_available_products()
        assert len(result) == 1
        assert result[0].stock == 5

    def test_get_available_products_todos_sin_stock(self, service, mock_product_repository):
        """Verifica que retorna lista vacía si ningún producto tiene stock."""
        mock_product_repository.get_all.return_value = [
            make_product(id=1, stock=0),
            make_product(id=2, stock=0),
        ]
        result = service.get_available_products()
        assert result == []

    def test_search_products_por_marca(self, service, mock_product_repository):
        """Verifica que filtra productos por marca."""
        mock_product_repository.get_by_brand.return_value = [make_product(brand="Nike")]
        result = service.search_products(brand="Nike")
        assert len(result) == 1
        mock_product_repository.get_by_brand.assert_called_once_with("Nike")

    def test_search_products_por_categoria(self, service, mock_product_repository):
        """Verifica que filtra productos por categoría."""
        mock_product_repository.get_by_category.return_value = [make_product(category="Running")]
        result = service.search_products(category="Running")
        assert len(result) == 1
        mock_product_repository.get_by_category.assert_called_once_with("Running")

    def test_search_products_sin_filtros(self, service, mock_product_repository):
        """Verifica que retorna todos los productos si no hay filtros."""
        mock_product_repository.get_all.return_value = [make_product(), make_product(id=2)]
        result = service.search_products()
        assert len(result) == 2

    def test_create_product(self, service, mock_product_repository):
        """Verifica que crea y retorna el producto con ID asignado."""
        mock_product_repository.save.return_value = make_product(id=10)
        dto = ProductDTO(
            id=None, name="Air Zoom", brand="Nike", category="Running",
            size="42", color="Negro", price=120.0, stock=5, description="Zapato"
        )
        result = service.create_product(dto)
        assert result.id == 10
        mock_product_repository.save.assert_called_once()

    def test_update_product_existente(self, service, mock_product_repository):
        """Verifica que actualiza correctamente un producto existente."""
        mock_product_repository.get_by_id.return_value = make_product(id=1)
        mock_product_repository.save.return_value = make_product(id=1, name="Nuevo Nombre")
        dto = ProductDTO(
            id=1, name="Nuevo Nombre", brand="Nike", category="Running",
            size="42", color="Negro", price=120.0, stock=5, description=""
        )
        result = service.update_product(1, dto)
        assert result.name == "Nuevo Nombre"

    def test_update_product_no_existente(self, service, mock_product_repository):
        """Verifica que lanza ProductNotFoundError al actualizar producto inexistente."""
        mock_product_repository.get_by_id.return_value = None
        dto = ProductDTO(
            id=99, name="X", brand="Y", category="Z",
            size="40", color="Rojo", price=50.0, stock=1, description=""
        )
        with pytest.raises(ProductNotFoundError):
            service.update_product(99, dto)

    def test_delete_product_existente(self, service, mock_product_repository):
        """Verifica que elimina correctamente un producto existente."""
        mock_product_repository.get_by_id.return_value = make_product(id=1)
        mock_product_repository.delete.return_value = True
        result = service.delete_product(1)
        assert result is True
        mock_product_repository.delete.assert_called_once_with(1)

    def test_delete_product_no_existente(self, service, mock_product_repository):
        """Verifica que lanza ProductNotFoundError al eliminar producto inexistente."""
        mock_product_repository.get_by_id.return_value = None
        with pytest.raises(ProductNotFoundError):
            service.delete_product(999)


# ─────────────────────────────────────────────
# Tests ChatService
# ─────────────────────────────────────────────

class TestChatService:
    """Tests para el servicio de chat."""

    @pytest.fixture
    def chat_service(self, mock_product_repository, mock_chat_repository, mock_ai_service):
        """Instancia de ChatService con dependencias mockeadas."""
        mock_ai_service.generate_response = AsyncMock(
            return_value="Tengo varios zapatos Nike disponibles."
        )
        mock_chat_repository.get_recent_messages = MagicMock(return_value=[])
        mock_chat_repository.save_message = MagicMock()
        mock_product_repository.get_all = MagicMock(return_value=[])
        return ChatService(
            product_repository=mock_product_repository,
            chat_repository=mock_chat_repository,
            ai_service=mock_ai_service
        )

    @pytest.mark.anyio
    async def test_process_message_retorna_respuesta(self, chat_service):
        """Verifica que process_message retorna un DTO con la respuesta de la IA."""
        request = ChatMessageRequestDTO(
            session_id="session_001",
            message="Busco zapatos Nike"
        )
        response = await chat_service.process_message(request)
        assert response.session_id == "session_001"
        assert response.user_message == "Busco zapatos Nike"
        assert response.assistant_message == "Tengo varios zapatos Nike disponibles."

    @pytest.mark.anyio
    async def test_process_message_guarda_dos_mensajes(self, chat_service, mock_chat_repository):
        """Verifica que se guardan el mensaje del usuario y el del asistente."""
        request = ChatMessageRequestDTO(session_id="session_001", message="Hola")
        await chat_service.process_message(request)
        assert mock_chat_repository.save_message.call_count == 2

    @pytest.mark.anyio
    async def test_process_message_consulta_productos(self, chat_service, mock_product_repository):
        """Verifica que se consultan los productos al procesar un mensaje."""
        request = ChatMessageRequestDTO(session_id="s1", message="¿Qué zapatos tienen?")
        await chat_service.process_message(request)
        mock_product_repository.get_all.assert_called_once()

    @pytest.mark.anyio
    async def test_process_message_consulta_historial(self, chat_service, mock_chat_repository):
        """Verifica que se recupera el historial reciente de la sesión."""
        request = ChatMessageRequestDTO(session_id="s1", message="Hola")
        await chat_service.process_message(request)
        mock_chat_repository.get_recent_messages.assert_called_once_with(
            session_id="s1", count=6
        )

    @pytest.mark.anyio
    async def test_process_message_lanza_error_si_falla_ia(
        self, mock_product_repository, mock_chat_repository, mock_ai_service
    ):
        """Verifica que se lanza ChatServiceError si la IA falla."""
        mock_ai_service.generate_response = AsyncMock(side_effect=Exception("Error de red"))
        mock_chat_repository.get_recent_messages = MagicMock(return_value=[])
        mock_product_repository.get_all = MagicMock(return_value=[])

        service = ChatService(
            product_repository=mock_product_repository,
            chat_repository=mock_chat_repository,
            ai_service=mock_ai_service
        )
        with pytest.raises(ChatServiceError):
            await service.process_message(
                ChatMessageRequestDTO(session_id="s1", message="Hola")
            )

    def test_get_session_history_retorna_mensajes(self, chat_service, mock_chat_repository):
        """Verifica que get_session_history retorna los mensajes de la sesión."""
        mock_chat_repository.get_session_history = MagicMock(return_value=[
            ChatMessage(id=1, session_id="s1", role="user",
                        message="Hola", timestamp=datetime.utcnow()),
            ChatMessage(id=2, session_id="s1", role="assistant",
                        message="¿En qué te ayudo?", timestamp=datetime.utcnow()),
        ])
        result = chat_service.get_session_history("s1", limit=10)
        assert len(result) == 2
        assert result[0].role == "user"
        assert result[1].role == "assistant"

    def test_get_session_history_lista_vacia(self, chat_service, mock_chat_repository):
        """Verifica que retorna lista vacía si no hay historial."""
        mock_chat_repository.get_session_history = MagicMock(return_value=[])
        result = chat_service.get_session_history("sesion_nueva")
        assert result == []

    def test_clear_session_history_retorna_cantidad(self, chat_service, mock_chat_repository):
        """Verifica que clear_session_history retorna la cantidad de mensajes eliminados."""
        mock_chat_repository.delete_session_history = MagicMock(return_value=5)
        result = chat_service.clear_session_history("s1")
        assert result == 5
        mock_chat_repository.delete_session_history.assert_called_once_with("s1")

    def test_clear_session_history_sin_mensajes(self, chat_service, mock_chat_repository):
        """Verifica que retorna 0 si no había mensajes que eliminar."""
        mock_chat_repository.delete_session_history = MagicMock(return_value=0)
        result = chat_service.clear_session_history("sesion_vacia")
        assert result == 0
