from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from src.infrastructure.db.database import get_db, init_db
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import (
    ProductDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO
)
from src.domain.exceptions import ProductNotFoundError
from datetime import datetime


app = FastAPI(
    title="E-commerce Chat AI",
    description="API REST de e-commerce de zapatos con chat inteligente usando Google Gemini.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Inicializa la base de datos y carga datos al arrancar la app."""
    init_db()


@app.get("/")
def root():
    """Retorna información básica de la API."""
    return {
        "name": "E-commerce Chat AI",
        "version": "1.0.0",
        "description": "API de e-commerce de zapatos con chat inteligente",
        "endpoints": {
            "products": "/products",
            "chat": "/chat",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Verifica que la API esté funcionando correctamente."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow()
    }


@app.get("/products", response_model=List[ProductDTO])
def get_products(db: Session = Depends(get_db)):
    """
    Lista todos los productos disponibles en el inventario.

    Returns:
        Lista de productos con todos sus atributos.
    """
    service = ProductService(SQLProductRepository(db))
    return service.get_all_products()


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su ID.

    Args:
        product_id: ID del producto a buscar.

    Raises:
        HTTPException 404: Si el producto no existe.
    """
    service = ProductService(SQLProductRepository(db))
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """
    Procesa un mensaje del usuario y retorna la respuesta de la IA.

    Args:
        request: DTO con session_id y mensaje del usuario.

    Raises:
        HTTPException 500: Si ocurre un error al procesar el mensaje.
    """
    try:
        service = ChatService(
            product_repository=SQLProductRepository(db),
            chat_repository=SQLChatRepository(db),
            ai_service=GeminiService()
        )
        return await service.process_message(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_chat_history(
    session_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de mensajes de una sesión.

    Args:
        session_id: Identificador de la sesión.
        limit: Número máximo de mensajes a retornar (default: 10).
    """
    service = ChatService(
        product_repository=SQLProductRepository(db),
        chat_repository=SQLChatRepository(db),
        ai_service=GeminiService()
    )
    return service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}")
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Elimina todo el historial de una sesión.

    Args:
        session_id: Identificador de la sesión a limpiar.

    Returns:
        Cantidad de mensajes eliminados.
    """
    service = ChatService(
        product_repository=SQLProductRepository(db),
        chat_repository=SQLChatRepository(db),
        ai_service=GeminiService()
    )
    deleted = service.clear_session_history(session_id)
    return {"deleted_messages": deleted}