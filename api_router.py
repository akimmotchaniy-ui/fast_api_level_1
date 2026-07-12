from fastapi import APIRouter, status

from fastapi import APIRouter, status

from schemas import TourCreateSchema, TourUpdateSchema, TourSavedSchema
from storage import storage

api_router = APIRouter(
    prefix='/api/tours'
)


@api_router.get('')
def list_tours() -> list[TourSavedSchema]:
    return storage.list_tours()


@api_router.get('/{tour_id}')
def get_tour(tour_id: str) -> TourSavedSchema:
    return storage.get_tour(tour_id)


@api_router.post('', status_code=status.HTTP_201_CREATED)
def create_tour(tour: TourCreateSchema) -> TourSavedSchema:
    return storage.create_tour(tour)


@api_router.patch('/{tour_id}')
def update_tour(tour_id: str, tour: TourUpdateSchema) -> TourSavedSchema:
    return storage.update_tour(tour_id, tour)


@api_router.delete('/{tour_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tour(tour_id: str) -> None:
    storage.delete_tour(tour_id)
