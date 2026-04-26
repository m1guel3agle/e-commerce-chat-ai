import os
from typing import List
import google.generativeai as genai
from src.domain.entities import Product, ChatContext


class GeminiService:
    """
    Servicio de IA que integra Google Gemini para el chat conversacional.

    Genera respuestas contextuales basadas en los productos
    disponibles y el historial de la conversación.
    """

    def __init__(self):
        """
        Inicializa el cliente de Gemini con la API key del entorno.

        Raises:
            ValueError: Si GEMINI_API_KEY no está configurada.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en .env")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate_response(
        self,
        user_message: str,
        products: List[Product],
        context: ChatContext
    ) -> str:
        """
        Genera una respuesta de IA basada en el mensaje y el contexto.

        Args:
            user_message: Mensaje actual del usuario.
            products: Lista de productos disponibles en el inventario.
            context: Contexto conversacional con mensajes recientes.

        Returns:
            Respuesta generada por Gemini como string.

        Raises:
            Exception: Si ocurre un error al llamar a la API de Gemini.
        """
        try:
            products_info = self.format_products_info(products)
            conversation_history = context.format_for_prompt()

            prompt = f"""Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_info}

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior para dar respuestas coherentes
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Responde siempre en español
- Si no tienes información sobre algo, sé honesto

CONVERSACIÓN ANTERIOR:
{conversation_history}

Usuario: {user_message}

Asistente:"""

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            raise Exception(f"Error al llamar a Gemini AI: {str(e)}")

    def format_products_info(self, products: List[Product]) -> str:
        """
        Convierte la lista de productos a texto legible para el prompt.

        Args:
            products: Lista de productos del inventario.

        Returns:
            String con los productos formateados, uno por línea.
        """
        if not products:
            return "No hay productos disponibles."

        lines = []
        for p in products:
            disponibilidad = "Disponible" if p.is_available() else "Agotado"
            lines.append(
                f"- {p.name} | {p.brand} | {p.category} | "
                f"Talla {p.size} | {p.color} | "
                f"${p.price} | Stock: {p.stock} | {disponibilidad}"
            )
        return "\n".join(lines)