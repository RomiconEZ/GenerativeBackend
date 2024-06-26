from fastcrud import FastCRUD

from ..models.waiting_customers import WaitingCustomers
from ..schemas.waiting_customers import (
    WaitingCustomersCreateInternal,
    WaitingCustomersDelete,
    WaitingCustomersUpdate,
    WaitingCustomersUpdateInternal,
)

CRUDWaitingCustomers = FastCRUD[
    WaitingCustomers,
    WaitingCustomersCreateInternal,
    WaitingCustomersUpdate,
    WaitingCustomersUpdateInternal,
    WaitingCustomersDelete,
]
crud_waiting_customers = CRUDWaitingCustomers(WaitingCustomers)
