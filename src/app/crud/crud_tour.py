from fastcrud import FastCRUD

from ..models.tour import Tour
from ..schemas.tour import (
    TourCreateInternal,
    TourDelete,
    TourUpdate,
    TourUpdateInternal,
)

CRUDTour = FastCRUD[Tour, TourCreateInternal, TourUpdate, TourUpdateInternal, TourDelete]
crud_tours = CRUDTour(Tour)
