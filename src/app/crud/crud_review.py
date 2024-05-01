from fastcrud import FastCRUD

from ..models.review import Review
from ..schemas.review import (
    ReviewCreateInternal,
    ReviewDelete,
    ReviewUpdate,
    ReviewUpdateInternal,
)

CRUDReview = FastCRUD[
    Review, ReviewCreateInternal, ReviewUpdate, ReviewUpdateInternal, ReviewDelete
]
crud_reviews = CRUDReview(Review)
