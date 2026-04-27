import pytest
from unittest.mock import MagicMock
from src.domain.entities import Product, ChatMessage, ChatContext
from datetime import datetime


@pytest.fixture
def sample_product():
    """Producto de ejemplo para usar en los tests."""
    return Product(
        id=1,
        name="Air Zoom Pegasus",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=120.0,
        stock=5,
        description="Zapato de running"
    )


@pytest.fixture
def sample_chat_message():
    """Mensaje de chat de ejemplo para usar en los tests."""
    return ChatMessage(
        id=1,
        session_id="session_test",
        role="user",
        message="Busco zapatos para correr",
        timestamp=datetime.utcnow()
    )

@pytest.fixture
def mock_product_repository():
    """Repositorio de productos mockeado."""
    return MagicMock()


@pytest.fixture
def mock_chat_repository():
    """Repositorio de chat mockeado."""
    return MagicMock()


@pytest.fixture
def mock_ai_service():
    """Servicio de IA mockeado."""
    return MagicMock()