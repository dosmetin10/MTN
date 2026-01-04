from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.core.database import session_scope
from app.models.stock import Product, StockMovement, StockMovementType, Warehouse
from app.schemas.stock import (
    ProductCreate,
    ProductRead,
    StockBalanceRead,
    StockMovementCreate,
    StockMovementRead,
    WarehouseCreate,
    WarehouseRead,
)
from app.services.stock import calculate_stock_balances

router = APIRouter()


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate) -> ProductRead:
    with session_scope() as session:
        product = Product(**payload.model_dump())
        session.add(product)
        session.flush()
        session.refresh(product)
        return ProductRead.model_validate(product)


@router.get("/products", response_model=list[ProductRead])
def list_products() -> list[ProductRead]:
    with session_scope() as session:
        products = session.exec(select(Product)).all()
        return [ProductRead.model_validate(product) for product in products]


@router.post("/warehouses", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
def create_warehouse(payload: WarehouseCreate) -> WarehouseRead:
    with session_scope() as session:
        warehouse = Warehouse(**payload.model_dump())
        session.add(warehouse)
        session.flush()
        session.refresh(warehouse)
        return WarehouseRead.model_validate(warehouse)


@router.get("/warehouses", response_model=list[WarehouseRead])
def list_warehouses() -> list[WarehouseRead]:
    with session_scope() as session:
        warehouses = session.exec(select(Warehouse)).all()
        return [WarehouseRead.model_validate(warehouse) for warehouse in warehouses]


@router.post("/movements", response_model=StockMovementRead, status_code=status.HTTP_201_CREATED)
def record_movement(payload: StockMovementCreate) -> StockMovementRead:
    with session_scope() as session:
        product = session.get(Product, payload.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        if payload.movement_type == StockMovementType.TRANSFER:
            if not (payload.source_warehouse_id and payload.target_warehouse_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transfer requires both source and target warehouses",
                )
            if payload.source_warehouse_id == payload.target_warehouse_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Source and target warehouse must differ for transfer",
                )
        elif payload.movement_type == StockMovementType.IN:
            if not payload.target_warehouse_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Target warehouse required for stock in movements",
                )
        elif payload.movement_type == StockMovementType.OUT:
            if not payload.source_warehouse_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Source warehouse required for stock out movements",
                )

        if payload.source_warehouse_id:
            source = session.get(Warehouse, payload.source_warehouse_id)
            if not source:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Source warehouse not found"
                )

        if payload.target_warehouse_id:
            target = session.get(Warehouse, payload.target_warehouse_id)
            if not target:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Target warehouse not found"
                )

        movement = StockMovement(**payload.model_dump())
        session.add(movement)
        session.flush()
        session.refresh(movement)
        return StockMovementRead.model_validate(movement)


@router.get("/movements", response_model=list[StockMovementRead])
def list_movements() -> list[StockMovementRead]:
    with session_scope() as session:
        movements = session.exec(select(StockMovement)).all()
        return [StockMovementRead.model_validate(movement) for movement in movements]


@router.get("/balances", response_model=list[StockBalanceRead])
def get_balances(
    product_id: int | None = None,
    warehouse_id: int | None = None,
) -> list[StockBalanceRead]:
    with session_scope() as session:
        return calculate_stock_balances(session, product_id=product_id, warehouse_id=warehouse_id)
