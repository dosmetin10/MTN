from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.core.database import session_scope
from app.models.customer import Account, Customer
from app.schemas.customer import CustomerCreate, CustomerRead

router = APIRouter()


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate) -> CustomerRead:
    with session_scope() as session:
        customer = Customer(**payload.model_dump())
        session.add(customer)
        session.flush()

        account = Account(customer_id=customer.id)
        session.add(account)
        session.refresh(customer)

        return CustomerRead.model_validate(customer)


@router.get("", response_model=list[CustomerRead])
def list_customers() -> list[CustomerRead]:
    with session_scope() as session:
        customers = session.exec(select(Customer)).all()
        return [CustomerRead.model_validate(customer) for customer in customers]


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int) -> CustomerRead:
    with session_scope() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return CustomerRead.model_validate(customer)
