from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency de FastAPI para obtener una sesión de base de datos.

    Usa yield para garantizar que la sesión se cierre
    siempre al terminar el request, incluso si hay errores.

    Yields:
        Sesión activa de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas
    y cargando los datos iniciales si no existen.
    """
    from src.infrastructure.db.models import ProductModel, ChatMemoryModel
    from src.infrastructure.db.init_data import load_initial_data

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        load_initial_data(db)
    finally:
        db.close()