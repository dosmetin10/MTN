from collections import defaultdict
from typing import Iterable, Optional

from sqlalchemy import or_  # type: ignore
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.stock import Product, StockMovement, StockMovementType, Warehouse
from app.schemas.stock import StockBalanceRead


def calculate_stock_balances(
    session: Session, *, product_id: Optional[int] = None, warehouse_id: Optional[int] = None
) -> list[StockBalanceRead]:
    """Aggregate stock balances per product/warehouse based on movements."""

    statement = select(StockMovement).options(
        selectinload(StockMovement.product),
        selectinload(StockMovement.source_warehouse),
        selectinload(StockMovement.target_warehouse),
    )

    if product_id is not None:
        statement = statement.where(StockMovement.product_id == product_id)

    if warehouse_id is not None:
        statement = statement.where(
            or_(
                StockMovement.source_warehouse_id == warehouse_id,
                StockMovement.target_warehouse_id == warehouse_id,
            )
        )

    movements: Iterable[StockMovement] = session.exec(statement).all()

    balances: defaultdict[tuple[int, Optional[int]], float] = defaultdict(float)
    product_names: dict[int, str] = {}
    warehouse_names: dict[int, str] = {}

    for movement in movements:
        product_names[movement.product_id] = movement.product.name if movement.product else ""

        if movement.source_warehouse:
            warehouse_names[movement.source_warehouse.id] = movement.source_warehouse.name
        if movement.target_warehouse:
            warehouse_names[movement.target_warehouse.id] = movement.target_warehouse.name

        if movement.movement_type == StockMovementType.IN:
            if movement.target_warehouse_id:
                balances[(movement.product_id, movement.target_warehouse_id)] += movement.quantity
        elif movement.movement_type == StockMovementType.OUT:
            if movement.source_warehouse_id:
                balances[(movement.product_id, movement.source_warehouse_id)] -= movement.quantity
        elif movement.movement_type == StockMovementType.TRANSFER:
            if movement.source_warehouse_id:
                balances[(movement.product_id, movement.source_warehouse_id)] -= movement.quantity
            if movement.target_warehouse_id:
                balances[(movement.product_id, movement.target_warehouse_id)] += movement.quantity

    return [
        StockBalanceRead(
            product_id=product_id_key,
            warehouse_id=warehouse_id_key,
            quantity=quantity,
            product_name=product_names.get(product_id_key),
            warehouse_name=warehouse_names.get(warehouse_id_key) if warehouse_id_key else None,
        )
        for (product_id_key, warehouse_id_key), quantity in balances.items()
    ]
