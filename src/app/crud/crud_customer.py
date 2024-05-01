from fastcrud import FastCRUD

from ..models.customer import Customer
from ..schemas.customer import (
    CustomerCreateInternal,
    CustomerDelete,
    CustomerUpdate,
    CustomerUpdateInternal,
)

CRUDCustomer = FastCRUD[
    Customer, CustomerCreateInternal, CustomerUpdate, CustomerUpdateInternal, CustomerDelete
]
crud_customers = CRUDCustomer(Customer)
