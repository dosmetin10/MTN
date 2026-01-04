from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.models.stock import StockMovementType


class ProductCreate(BaseModel):
    name: str
    sku: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = "adet"
    currency: Optional[str] = "TRY"
    price: float = Field(default=0.0, ge=0)
    track_inventory: bool = True

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, v: Optional[str]) -> Optional[str]:
        return v.upper() if v else v


class ProductRead(BaseModel):
    id: int
    name: str
    sku: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    currency: Optional[str] = None
    price: float
    track_inventory: bool

    class Config:
        from_attributes = True


class WarehouseCreate(BaseModel):
    name: str
    location: Optional[str] = None


class WarehouseRead(BaseModel):
    id: int
    name: str
    location: Optional[str] = None

    class Config:
        from_attributes = True


class StockMovementCreate(BaseModel):
    movement_type: StockMovementType
    quantity: float = Field(gt=0)
    note: Optional[str] = None
    product_id: int
    source_warehouse_id: Optional[int] = None
    target_warehouse_id: Optional[int] = None


class StockMovementRead(BaseModel):
    id: int
    movement_type: StockMovementType
    quantity: float
    note: Optional[str] = None
    product_id: int
    source_warehouse_id: Optional[int] = None
    target_warehouse_id: Optional[int] = None

    class Config:
        from_attributes = True


class StockBalanceRead(BaseModel):
    product_id: int
    warehouse_id: Optional[int] = None
    quantity: float
    product_name: Optional[str] = None
    warehouse_name: Optional[str] = None
