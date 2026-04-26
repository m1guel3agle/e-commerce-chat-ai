from src.infrastructure.db.models import ProductModel


def load_initial_data(db):
    """
    Carga productos de ejemplo si la base de datos está vacía.

    Verifica si ya existen productos antes de insertar
    para evitar duplicados al reiniciar la aplicación.

    Args:
        db: Sesión activa de SQLAlchemy.
    """
    count = db.query(ProductModel).count()
    if count > 0:
        return

    products = [
        ProductModel(
            name="Air Zoom Pegasus 40",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato de running con amortiguación reactiva ideal para largas distancias."
        ),
        ProductModel(
            name="Ultraboost 23",
            brand="Adidas",
            category="Running",
            size="41",
            color="Blanco",
            price=150.0,
            stock=3,
            description="Alto rendimiento con tecnología Boost para máxima energía de retorno."
        ),
        ProductModel(
            name="Suede Classic XXI",
            brand="Puma",
            category="Casual",
            size="40",
            color="Azul",
            price=80.0,
            stock=10,
            description="Clásico urbano con diseño atemporal, perfecto para el día a día."
        ),
        ProductModel(
            name="Chuck Taylor All Star",
            brand="Converse",
            category="Casual",
            size="43",
            color="Rojo",
            price=65.0,
            stock=8,
            description="Icónico zapato de lona con suela de goma vulcanizada."
        ),
        ProductModel(
            name="Gel-Kayano 30",
            brand="Asics",
            category="Running",
            size="44",
            color="Gris",
            price=160.0,
            stock=4,
            description="Estabilidad y soporte superior para corredores de alto rendimiento."
        ),
        ProductModel(
            name="Old Skool",
            brand="Vans",
            category="Casual",
            size="41",
            color="Negro/Blanco",
            price=70.0,
            stock=12,
            description="Diseño skate clásico con la icónica raya lateral de Vans."
        ),
        ProductModel(
            name="Fresh Foam X 1080v12",
            brand="New Balance",
            category="Running",
            size="42",
            color="Azul marino",
            price=175.0,
            stock=2,
            description="Máxima amortiguación para carreras de larga distancia."
        ),
        ProductModel(
            name="Clarks Desert Boot",
            brand="Clarks",
            category="Formal",
            size="43",
            color="Camel",
            price=130.0,
            stock=6,
            description="Bota de ante con suela de crepé, elegante y versátil."
        ),
        ProductModel(
            name="Stan Smith",
            brand="Adidas",
            category="Casual",
            size="40",
            color="Blanco/Verde",
            price=90.0,
            stock=9,
            description="Tenis minimalista con diseño limpio y atemporal."
        ),
        ProductModel(
            name="Air Force 1 '07",
            brand="Nike",
            category="Casual",
            size="44",
            color="Blanco",
            price=110.0,
            stock=7,
            description="El clásico de baloncesto reconvertido en ícono de la cultura urbana."
        ),
    ]

    db.add_all(products)
    db.commit()
    print("Datos iniciales cargados correctamente.")