from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel


class StockMovementType(str, Enum):
    IN = "in"
    OUT = "out"
    TRANSFER = "transfer"


class ProductBase(SQLModel):
    name: str
    sku: Optional[str] = Field(default=None, index=True)
    category: Optional[str] = None
    unit: Optional[str] = Field(default="adet")
    currency: Optional[str] = Field(default="TRY", max_length=3)
    price: float = Field(default=0.0, ge=0)
    track_inventory: bool = Field(default=True)


class Product(ProductBase, TimestampedModel, IDModel, table=True):
    __tablename__ = "products"

    movements: list["StockMovement"] = Relationship(back_populates="product")


class WarehouseBase(SQLModel):
    name: str
    location: Optional[str] = None


class Warehouse(WarehouseBase, TimestampedModel, IDModel, table=True):
    __tablename__ = "warehouses"

    outgoing_movements: list["StockMovement"] = Relationship(
        back_populates="source_warehouse",
        sa_relationship_kwargs={"foreign_keys": "StockMovement.source_warehouse_id"},
    )
    incoming_movements: list["StockMovement"] = Relationship(
        back_populates="target_warehouse",
        sa_relationship_kwargs={"foreign_keys": "StockMovement.target_warehouse_id"},
    )


class StockMovementBase(SQLModel):
    movement_type: StockMovementType
    quantity: float = Field(gt=0)
    note: Optional[str] = None

    product_id: int = Field(foreign_key="products.id")
    source_warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouses.id")
    target_warehouse_id: Optional[int] = Field(default=None, foreign_key="warehouses.id")


class StockMovement(StockMovementBase, TimestampedModel, IDModel, table=True):
    __tablename__ = "stock_movements"

    product: Optional[Product] = Relationship(back_populates="movements")
    source_warehouse: Optional[Warehouse] = Relationship(
        back_populates="outgoing_movements",
        sa_relationship_kwargs={"foreign_keys": "StockMovement.source_warehouse_id"},
    )
    target_warehouse: Optional[Warehouse] = Relationship(
        back_populates="incoming_movements",
        sa_relationship_kwargs={"foreign_keys": "StockMovement.target_warehouse_id"},
    )
