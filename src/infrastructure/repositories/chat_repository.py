from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """
    Implementación concreta del repositorio de chat usando SQLAlchemy.

    Gestiona la persistencia del historial de conversaciones
    en la tabla chat_memory de SQLite.

    Atributos:
        db: Sesión activa de SQLAlchemy.
    """

    def __init__(self, db: Session):
        """
        Args:
            db: Sesión de base de datos inyectada.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje en el historial."""
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """Obtiene el historial de una sesión en orden cronológico."""
        query = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp.asc())

        if limit:
            query = query.limit(limit)

        return [self._model_to_entity(m) for m in query.all()]

    def delete_session_history(self, session_id: str) -> int:
        """Elimina todo el historial de una sesión."""
        deleted = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).delete()
        self.db.commit()
        return deleted

    def get_recent_messages(
        self, session_id: str, count: int
    ) -> List[ChatMessage]:
        """Obtiene los últimos N mensajes en orden cronológico."""
        models = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp.desc()).limit(count).all()

        models.reverse()
        return [self._model_to_entity(m) for m in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """Convierte un modelo ORM a entidad del dominio."""
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """Convierte una entidad del dominio a modelo ORM."""
        return ChatMemoryModel(
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp
        )