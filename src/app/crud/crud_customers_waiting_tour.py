from fastcrud import FastCRUD

from ..models.customers_waiting_tour import CustomersWaitingTour
from ..schemas.customers_waiting_tour import (
    CustomersWaitingTourCreateInternal,
    CustomersWaitingTourDelete,
    CustomersWaitingTourUpdate,
    CustomersWaitingTourUpdateInternal,
)

CRUDCustomersWaitingTour = FastCRUD[
    CustomersWaitingTour,
    CustomersWaitingTourCreateInternal,
    CustomersWaitingTourUpdate,
    CustomersWaitingTourUpdateInternal,
    CustomersWaitingTourDelete,
]
crud_customers_waiting_tour = CRUDCustomersWaitingTour(CustomersWaitingTour)