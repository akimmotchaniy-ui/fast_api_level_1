from fastapi import APIRouter, status

from schemas import TourCreateSchema, TourUpdateSchema, TourSavedSchema
from storage import storage

api_router = APIRouter(
    prefix='/api/tours'
)


@api_router.get('')
def index_tours() -> list[TourSavedSchema]:
    """переглянути всі тури"""
    return storage.get_all_tours()


@api_router.get('/{tour_id}')
def get_tour(tour_id: str) -> TourSavedSchema:
    """переглянути конкретний тур"""
    tour = storage.get_tour(tour_id)
    return tour


@api_router.post('', status_code=status.HTTP_201_CREATED)
def create_tour(tour: TourCreateSchema) -> TourSavedSchema:
    """the single endpoint for creating tour in storage"""
    created_tour = storage.create_tour(tour)
    return created_tour


@api_router.put('/{tour_id}')
def update_tour(tour_id: str, tour: TourUpdateSchema) -> TourSavedSchema:
    """відредагувати конкретний тур"""
    updated_tour = storage.update_tour(tour_id, tour)
    return updated_tour


@api_router.delete('/{tour_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tour(tour_id: str) -> None:
    """видалити конкретний тур"""
    storage.delete_tour(tour_id)
