from abc import ABC, abstractmethod
from datetime import datetime, date

from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException, status

from schemas import TourCreateSchema, TourUpdateSchema, TourSavedSchema
from settings import settings


class BaseStorage(ABC):

    @abstractmethod
    def create_tour(self, tour: TourCreateSchema) -> TourSavedSchema: ...

    @abstractmethod
    def get_tour(self, tour_id: str) -> TourSavedSchema: ...

    @abstractmethod
    def list_tours(self) -> list[TourSavedSchema]: ...

    @abstractmethod
    def update_tour(self, tour_id: str, tour: TourUpdateSchema) -> TourSavedSchema: ...

    @abstractmethod
    def delete_tour(self, tour_id: str) -> None: ...


def _validate_id(tour_id: str) -> ObjectId:
    if not ObjectId.is_valid(tour_id):
        raise HTTPException(
            detail=f"Invalid tour id '{tour_id}'",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return ObjectId(tour_id)


def _serialize_dates(data: dict) -> dict:
    """Convert date to datetime because pymongo can't store date directly."""
    for key, value in data.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            data[key] = datetime.combine(value, datetime.min.time())
    return data


class MongoStorage(BaseStorage):
    def __init__(self):
        client = MongoClient(settings.URI)
        database = client[settings.DB_NAME]
        self.collection = database[settings.TOURS_COLLECTION]

    def _to_schema(self, raw: dict) -> TourSavedSchema:
        return TourSavedSchema(
            id=str(raw['_id']),
            title=raw['title'],
            country=raw['country'],
            price=raw['price'],
            duration_days=raw['duration_days'],
            start_date=raw['start_date'],
            description=raw.get('description', ''),
            created_at=raw['created_at'],
        )

    def create_tour(self, tour: TourCreateSchema) -> TourSavedSchema:
        tour_dict = tour.model_dump()
        tour_dict = _serialize_dates(tour_dict)
        tour_dict['created_at'] = datetime.now()

        result = self.collection.insert_one(document=tour_dict)
        return self.get_tour(str(result.inserted_id))

    def get_tour(self, tour_id: str) -> TourSavedSchema:
        object_id = _validate_id(tour_id)
        raw = self.collection.find_one({'_id': object_id})
        if not raw:
            raise HTTPException(
                detail=f"Tour with id '{tour_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return self._to_schema(raw)

    def list_tours(self) -> list[TourSavedSchema]:
        raw_tours = self.collection.find().sort('created_at', -1)
        return [self._to_schema(raw) for raw in raw_tours]

    def update_tour(self, tour_id: str, tour: TourUpdateSchema) -> TourSavedSchema:
        object_id = _validate_id(tour_id)
        update_data = tour.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                detail="No fields to update",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        update_data = _serialize_dates(update_data)

        result = self.collection.update_one(
            {'_id': object_id},
            {'$set': update_data},
        )
        if result.matched_count == 0:
            raise HTTPException(
                detail=f"Tour with id '{tour_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return self.get_tour(tour_id)

    def delete_tour(self, tour_id: str) -> None:
        object_id = _validate_id(tour_id)
        result = self.collection.delete_one({'_id': object_id})
        if result.deleted_count == 0:
            raise HTTPException(
                detail=f"Tour with id '{tour_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )


storage: BaseStorage = MongoStorage()
