# E-commerce Chat AI 🤖👟

API REST de e-commerce de zapatos con chat inteligente powered by Google Gemini. Permite a los usuarios consultar productos y conversar con un asistente de IA que recuerda el contexto de la conversación.

---

## Características Principales

- Listado y búsqueda de productos (zapatos) por ID
- Chat conversacional con IA usando Google Gemini
- Memoria conversacional por sesión (últimos 6 mensajes)
- Persistencia de historial de chat en base de datos
- Arquitectura limpia en 3 capas (Domain, Application, Infrastructure)
- Documentación automática con Swagger UI
- Containerización con Docker

---

## Arquitectura

El proyecto implementa **Clean Architecture** con 3 capas bien definidas:

```
┌─────────────────────────────────────────┐
│         INFRASTRUCTURE LAYER            │
│  FastAPI · SQLAlchemy · GeminiService   │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│          APPLICATION LAYER              │
│     ProductService · ChatService        │
│         DTOs con Pydantic               │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│            DOMAIN LAYER                 │
│   Product · ChatMessage · ChatContext   │
│   IProductRepository · IChatRepository  │
└─────────────────────────────────────────┘
```

---

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|---|---|---|
| Python | 3.10+ | Lenguaje base |
| FastAPI | 0.115.0 | Framework web y endpoints HTTP |
| Uvicorn | 0.30.0 | Servidor ASGI |
| SQLAlchemy | 2.0.36 | ORM y acceso a base de datos |
| Pydantic | 2.9.0 | Validación de datos y DTOs |
| pydantic-settings | 2.1.0 | Gestión de variables de entorno |
| python-dotenv | 1.0.0 | Carga de archivo .env |
| Google Generative AI | 0.8.0 | Integración con Gemini AI |
| SQLite | — | Base de datos ligera |
| Docker | — | Containerización |
| Pytest | 7.4.3 | Testing unitario |

---

## Estructura del Proyecto

```
e-commerce-chat-ai/
│
├── src/
│   ├── config.py
│   ├── domain/
│   │   ├── entities.py          # Product, ChatMessage, ChatContext
│   │   ├── repositories.py      # IProductRepository, IChatRepository
│   │   └── exceptions.py        # Excepciones del dominio
│   ├── application/
│   │   ├── dtos.py              # DTOs con Pydantic
│   │   ├── product_service.py   # Casos de uso de productos
│   │   └── chat_service.py      # Casos de uso de chat
│   └── infrastructure/
│       ├── api/
│       │   └── main.py          # Aplicación FastAPI
│       ├── db/
│       │   ├── database.py      # Configuración SQLAlchemy
│       │   ├── models.py        # Modelos ORM
│       │   └── init_data.py     # Datos iniciales
│       ├── repositories/
│       │   ├── product_repository.py
│       │   └── chat_repository.py
│       └── llm_providers/
│           └── gemini_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_entities.py
│   └── test_services.py
│
├── data/                        # Base de datos SQLite (auto-generada)
├── evidencias/                  # Screenshots de evidencia
├── .env                         # Variables de entorno (no versionar)
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Requisitos Previos

- Python 3.10 o superior
- Docker y Docker Compose
- API Key de Google Gemini ([obtener aquí](https://ai.google.dev/))

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/m1guel3agle/e-commerce-chat-ai
cd e-commerce-chat-ai
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar el archivo `.env` y agregar tu API Key de Gemini:

```env
GEMINI_API_KEY=tu_api_key_aqui
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development
```

### 3. Instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 4. Ejecutar localmente

```bash
uvicorn src.infrastructure.api.main:app --reload
```

La API estará disponible en `http://localhost:8000`

---

## Uso con Docker

### Construir y levantar el contenedor

```bash
docker-compose up --build
```

### Verificar que está corriendo

```bash
docker ps
```

### Ver logs

```bash
docker-compose logs -f
```

### Detener el contenedor

```bash
docker-compose down
```

---

## Endpoints

### Información general

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| GET | `/docs` | Documentación Swagger UI |

### Productos

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/products` | Lista todos los productos |
| GET | `/products/{id}` | Obtiene un producto por ID |

### Chat

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/chat` | Envía un mensaje al asistente de IA |
| GET | `/chat/history/{session_id}` | Obtiene el historial de una sesión |
| DELETE | `/chat/history/{session_id}` | Elimina el historial de una sesión |

### Ejemplos de uso

**Listar productos:**
```bash
curl http://localhost:8000/products
```

**Obtener producto por ID:**
```bash
curl http://localhost:8000/products/1
```

**Enviar mensaje al chat:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "usuario_001",
    "message": "Busco zapatos Nike para correr talla 42"
  }'
```

**Ver historial de conversación:**
```bash
curl http://localhost:8000/chat/history/usuario_001
```

**Eliminar historial:**
```bash
curl -X DELETE http://localhost:8000/chat/history/usuario_001
```

---

## Testing

### Ejecutar todos los tests

```bash
pytest -v
```

### Ejecutar con reporte de coverage

```bash
pytest --cov=src --cov-report=term-missing
```

El proyecto cuenta con **92% de coverage** sobre las capas de dominio y aplicación.

---

## Documentación Interactiva

Una vez levantada la API, la documentación está disponible en:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Autor

**Miguel Angel Aguilar** — Universidad EAFIT
