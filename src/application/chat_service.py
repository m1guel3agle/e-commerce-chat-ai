from datetime import datetime
from typing import List, Optional
from src.domain.entities import ChatMessage, ChatContext
from src.domain.repositories import IProductRepository, IChatRepository
from src.domain.exceptions import ChatServiceError
from src.application.dtos import (
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO
)


class ChatService:
    """
    Servicio de aplicación para el chat con IA.

    Orquesta el flujo completo de una conversación:
    obtiene productos, recupera historial, llama a la IA
    y guarda los mensajes resultantes.

    Atributos:
        product_repository: Repositorio de productos.
        chat_repository: Repositorio del historial de chat.
        ai_service: Servicio de IA (GeminiService).
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service
    ):
        """
        Args:
            product_repository: Repositorio de productos inyectado.
            chat_repository: Repositorio de chat inyectado.
            ai_service: Servicio de IA inyectado (GeminiService).
        """
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.ai_service = ai_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta con IA.

        Flujo:
        1. Obtiene todos los productos disponibles.
        2. Recupera los últimos 6 mensajes de la sesión.
        3. Crea el ChatContext con el historial.
        4. Llama a la IA con mensaje + productos + contexto.
        5. Guarda el mensaje del usuario en el repositorio.
        6. Guarda la respuesta del asistente en el repositorio.
        7. Retorna el DTO con ambos mensajes.

        Args:
            request: DTO con session_id y mensaje del usuario.

        Returns:
            DTO con el mensaje del usuario y la respuesta de la IA.

        Raises:
            ChatServiceError: Si ocurre un error al procesar el mensaje.
        """
        try:
            products = self.product_repository.get_all()

            recent_messages = self.chat_repository.get_recent_messages(
                session_id=request.session_id,
                count=6
            )

            context = ChatContext(messages=recent_messages)

            ai_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context
            )

            timestamp = datetime.utcnow()

            user_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role='user',
                message=request.message,
                timestamp=timestamp
            )
            self.chat_repository.save_message(user_message)

            assistant_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role='assistant',
                message=ai_response,
                timestamp=timestamp
            )
            self.chat_repository.save_message(assistant_message)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=ai_response,
                timestamp=timestamp
            )

        except Exception as e:
            raise ChatServiceError(
                f"Error al procesar el mensaje: {str(e)}"
            )

    def get_session_history(
        self, session_id: str, limit: Optional[int] = 10
    ) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de mensajes de una sesión.

        Args:
            session_id: Identificador de la sesión.
            limit: Número máximo de mensajes a retornar.

        Returns:
            Lista de mensajes del historial como DTOs.
        """
        messages = self.chat_repository.get_session_history(
            session_id=session_id,
            limit=limit
        )
        return [
            ChatHistoryDTO(
                id=msg.id,
                role=msg.role,
                message=msg.message,
                timestamp=msg.timestamp
            )
            for msg in messages
        ]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Args:
            session_id: Identificador de la sesión a limpiar.

        Returns:
            Cantidad de mensajes eliminados.
        """
        return self.chat_repository.delete_session_history(session_id)