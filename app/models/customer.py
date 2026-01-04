from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IDModel, TimestampedModel

if TYPE_CHECKING:  # pragma: no cover
    from app.models.customer import Account as AccountType


class CustomerBase(SQLModel):
    name: str
    title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    tax_office: Optional[str] = None
    tax_number: Optional[str] = None
    currency: Optional[str] = Field(default="TRY", max_length=3)
    notes: Optional[str] = None


class Customer(CustomerBase, TimestampedModel, IDModel, table=True):
    __tablename__ = "customers"

    accounts: list["Account"] = Relationship(back_populates="customer")


class Account(SQLModel, TimestampedModel, IDModel, table=True):
    __tablename__ = "accounts"

    customer_id: int = Field(foreign_key="customers.id")
    balance: float = Field(default=0.0)

    customer: Optional[Customer] = Relationship(back_populates="accounts")
