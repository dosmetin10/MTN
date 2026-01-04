from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class CustomerCreate(BaseModel):
    name: str
    title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    tax_office: Optional[str] = None
    tax_number: Optional[str] = None
    currency: Optional[str] = "TRY"
    notes: Optional[str] = None

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, v: Optional[str]) -> Optional[str]:
        return v.upper() if v else v


class CustomerRead(BaseModel):
    id: int
    name: str
    title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    tax_office: Optional[str] = None
    tax_number: Optional[str] = None
    currency: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
