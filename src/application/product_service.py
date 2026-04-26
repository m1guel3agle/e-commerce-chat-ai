from typing import List, Optional
from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.domain.exceptions import ProductNotFoundError
from src.application.dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para la gestión de productos.

    Orquesta los casos de uso relacionados con productos,
    usando el repositorio inyectado para acceder a los datos.

    Atributos:
        repository: Repositorio de productos inyectado.
    """

    def __init__(self, repository: IProductRepository):
        """
        Args:
            repository: Implementación del repositorio de productos.
        """
        self.repository = repository

    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos disponibles.

        Returns:
            Lista de productos como DTOs.
        """
        products = self.repository.get_all()
        return [self._entity_to_dto(p) for p in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Obtiene un producto por su ID.

        Args:
            product_id: ID del producto a buscar.

        Returns:
            El producto como DTO.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return self._entity_to_dto(product)

    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene solo los productos con stock disponible.

        Returns:
            Lista de productos disponibles como DTOs.
        """
        products = self.repository.get_all()
        available = [p for p in products if p.is_available()]
        return [self._entity_to_dto(p) for p in available]

    def search_products(
        self, brand: Optional[str] = None, category: Optional[str] = None
    ) -> List[ProductDTO]:
        """
        Filtra productos por marca y/o categoría.

        Args:
            brand: Marca por la que filtrar (opcional).
            category: Categoría por la que filtrar (opcional).

        Returns:
            Lista de productos filtrados como DTOs.
        """
        if brand:
            products = self.repository.get_by_brand(brand)
        elif category:
            products = self.repository.get_by_category(category)
        else:
            products = self.repository.get_all()
        return [self._entity_to_dto(p) for p in products]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto en el repositorio.

        Args:
            product_dto: DTO con los datos del nuevo producto.

        Returns:
            El producto creado con su ID asignado.
        """
        entity = self._dto_to_entity(product_dto)
        saved = self.repository.save(entity)
        return self._entity_to_dto(saved)

    def update_product(
        self, product_id: int, product_dto: ProductDTO
    ) -> ProductDTO:
        """
        Actualiza un producto existente.

        Args:
            product_id: ID del producto a actualizar.
            product_dto: DTO con los nuevos datos.

        Returns:
            El producto actualizado como DTO.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        existing = self.repository.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(product_id)
        entity = self._dto_to_entity(product_dto)
        entity.id = product_id
        saved = self.repository.save(entity)
        return self._entity_to_dto(saved)

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto del repositorio.

        Args:
            product_id: ID del producto a eliminar.

        Returns:
            True si se eliminó correctamente.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        existing = self.repository.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(product_id)
        return self.repository.delete(product_id)

    def _entity_to_dto(self, product: Product) -> ProductDTO:
        """Convierte una entidad Product a ProductDTO."""
        return ProductDTO(
            id=product.id,
            name=product.name,
            brand=product.brand,
            category=product.category,
            size=product.size,
            color=product.color,
            price=product.price,
            stock=product.stock,
            description=product.description
        )

    def _dto_to_entity(self, dto: ProductDTO) -> Product:
        """Convierte un ProductDTO a entidad Product."""
        return Product(
            id=dto.id,
            name=dto.name,
            brand=dto.brand,
            category=dto.category,
            size=dto.size,
            color=dto.color,
            price=dto.price,
            stock=dto.stock,
            description=dto.description
        )