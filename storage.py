from pymongo import MongoClient
from bson import ObjectId

from schemas import TourCreateSchema, TourUpdateSchema, TourSavedSchema
from settings import settings
from abc import ABC, abstractmethod
from datetime import datetime
from fastapi import HTTPException, status


class BaseStorage(ABC):

    @abstractmethod
    def create_tour(self, tour: TourCreateSchema) -> TourSavedSchema:
        return

    @abstractmethod
    def get_tour(self, tour_id: str) -> TourSavedSchema:
        return

    @abstractmethod
    def get_all_tours(self) -> list[TourSavedSchema]:
        return

    @abstractmethod
    def update_tour(self, tour_id: str, tour: TourUpdateSchema) -> TourSavedSchema:
        return

    @abstractmethod
    def delete_tour(self, tour_id: str) -> None:
        return


class MongoStorage(BaseStorage):
    def __init__(self):
        client = MongoClient(settings.URI)
        database = client[settings.DB_NAME]
        self.collection = database[settings.TOURS_COLLECTION]

    def _check_valid_id(self, tour_id: str) -> ObjectId:
        if not ObjectId.is_valid(tour_id):
            raise HTTPException(
                detail=f"Invalid tour id '{tour_id}'",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return ObjectId(tour_id)

    def get_tour(self, tour_id: str | ObjectId) -> TourSavedSchema:
        object_id = self._check_valid_id(tour_id) if isinstance(tour_id, str) else tour_id
        query = {
            '_id': object_id
        }
        raw_tour = self.collection.find_one(query)
        if not raw_tour:
            raise HTTPException(
                detail=f"Tour with id '{tour_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        tour = TourSavedSchema(
            id=str(raw_tour['_id']),
            **{k: v for k, v in raw_tour.items() if k != '_id'}
        )
        return tour

    def get_all_tours(self) -> list[TourSavedSchema]:
        raw_tours = self.collection.find()
        tours = [
            TourSavedSchema(
                id=str(raw_tour['_id']),
                **{k: v for k, v in raw_tour.items() if k != '_id'}
            )
            for raw_tour in raw_tours
        ]
        return tours

    def create_tour(self, tour: TourCreateSchema) -> TourSavedSchema:
        tour_dict = tour.model_dump()
        tour_dict['created_at'] = datetime.now()

        result = self.collection.insert_one(document=tour_dict)
        tour_id = result.inserted_id

        saved = self.get_tour(tour_id)
        return saved

    def update_tour(self, tour_id: str, tour: TourUpdateSchema) -> TourSavedSchema:
        object_id = self._check_valid_id(tour_id)

        update_data = {k: v for k, v in tour.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(
                detail='No fields provided to update',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        result = self.collection.update_one(
            {'_id': object_id},
            {'$set': update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(
                detail=f"Tour with id '{tour_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return self.get_tour(object_id)

    def delete_tour(self, tour_id: str) -> None:
        object_id = self._check_valid_id(tour_id)

        result = self.collection.delete_one({'_id': object_id})
        if result.deleted_count == 0:
            raise HTTPException(
                detail=f"Tour with id '{tour_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND
            )


storage: BaseStorage = MongoStorage()
