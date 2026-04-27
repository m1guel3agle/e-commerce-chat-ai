import pytest
from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext


class TestProduct:
    """Tests para la entidad Product."""

    def test_crear_producto_valido(self):
        """Verifica que se puede crear un producto con datos válidos."""
        product = Product(
            id=1, name="Air Zoom", brand="Nike", category="Running",
            size="42", color="Negro", price=120.0, stock=5,
            description="Zapato running"
        )
        assert product.name == "Air Zoom"
        assert product.price == 120.0
        assert product.stock == 5

    def test_precio_negativo_lanza_error(self):
        """Verifica que precio negativo lanza ValueError."""
        with pytest.raises(ValueError):
            Product(
                id=None, name="X", brand="Y", category="Z",
                size="40", color="Rojo", price=-10, stock=5,
                description=""
            )

    def test_stock_negativo_lanza_error(self):
        """Verifica que stock negativo lanza ValueError."""
        with pytest.raises(ValueError):
            Product(
                id=None, name="X", brand="Y", category="Z",
                size="40", color="Rojo", price=50, stock=-1,
                description=""
            )

    def test_nombre_vacio_lanza_error(self):
        """Verifica que nombre vacío lanza ValueError."""
        with pytest.raises(ValueError):
            Product(
                id=None, name="", brand="Y", category="Z",
                size="40", color="Rojo", price=50, stock=5,
                description=""
            )

    def test_is_available_con_stock(self, sample_product):
        """Verifica que is_available retorna True cuando hay stock."""
        assert sample_product.is_available() is True

    def test_is_available_sin_stock(self, sample_product):
        """Verifica que is_available retorna False cuando no hay stock."""
        sample_product.stock = 0
        assert sample_product.is_available() is False

    def test_reduce_stock_correcto(self, sample_product):
        """Verifica que reduce_stock descuenta correctamente."""
        sample_product.reduce_stock(2)
        assert sample_product.stock == 3

    def test_reduce_stock_insuficiente_lanza_error(self, sample_product):
        """Verifica que reduce_stock lanza error si no hay suficiente stock."""
        with pytest.raises(ValueError):
            sample_product.reduce_stock(100)

    def test_increase_stock_correcto(self, sample_product):
        """Verifica que increase_stock suma correctamente."""
        sample_product.increase_stock(10)
        assert sample_product.stock == 15

    def test_increase_stock_negativo_lanza_error(self, sample_product):
        """Verifica que increase_stock lanza error con cantidad negativa."""
        with pytest.raises(ValueError):
            sample_product.increase_stock(-5)


class TestChatMessage:
    """Tests para la entidad ChatMessage."""

    def test_crear_mensaje_valido(self):
        """Verifica que se puede crear un mensaje válido."""
        msg = ChatMessage(
            id=1, session_id="s1", role="user",
            message="Hola", timestamp=datetime.utcnow()
        )
        assert msg.role == "user"
        assert msg.message == "Hola"

    def test_role_invalido_lanza_error(self):
        """Verifica que un rol inválido lanza ValueError."""
        with pytest.raises(ValueError):
            ChatMessage(
                id=1, session_id="s1", role="admin",
                message="Hola", timestamp=datetime.utcnow()
            )

    def test_mensaje_vacio_lanza_error(self):
        """Verifica que mensaje vacío lanza ValueError."""
        with pytest.raises(ValueError):
            ChatMessage(
                id=1, session_id="s1", role="user",
                message="", timestamp=datetime.utcnow()
            )

    def test_is_from_user(self, sample_chat_message):
        """Verifica que is_from_user retorna True para mensajes de usuario."""
        assert sample_chat_message.is_from_user() is True
        assert sample_chat_message.is_from_assistant() is False

    def test_is_from_assistant(self):
        """Verifica que is_from_assistant retorna True para mensajes de asistente."""
        msg = ChatMessage(
            id=2, session_id="s1", role="assistant",
            message="Hola, te ayudo", timestamp=datetime.utcnow()
        )
        assert msg.is_from_assistant() is True
        assert msg.is_from_user() is False


class TestChatContext:
    """Tests para el value object ChatContext."""

    def test_get_recent_messages_limita_cantidad(self):
        """Verifica que get_recent_messages retorna solo los últimos N mensajes."""
        messages = [
            ChatMessage(
                id=i, session_id="s1", role="user",
                message=f"Mensaje {i}", timestamp=datetime.utcnow()
            )
            for i in range(1, 10)
        ]
        ctx = ChatContext(messages=messages, max_messages=6)
        recent = ctx.get_recent_messages()
        assert len(recent) == 6

    def test_format_for_prompt(self):
        """Verifica que format_for_prompt genera el formato correcto."""
        messages = [
            ChatMessage(id=1, session_id="s1", role="user",
                       message="Hola", timestamp=datetime.utcnow()),
            ChatMessage(id=2, session_id="s1", role="assistant",
                       message="¿En qué te ayudo?", timestamp=datetime.utcnow()),
        ]
        ctx = ChatContext(messages=messages)
        result = ctx.format_for_prompt()
        assert "Usuario: Hola" in result
        assert "Asistente: ¿En qué te ayudo?" in result