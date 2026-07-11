from pymongo import MongoClient
from bson import ObjectId

from schemas import BookCreateSchema, BookSavedSchema
from settings import settings
from abc import ABC, abstractmethod
from datetime import datetime
from fastapi import HTTPException, status

class BaseStorage(ABC):

    @abstractmethod
    def create_book(self, book: BookCreateSchema) -> BookSavedSchema:
        return

    @abstractmethod
    def get_book(self, book_id: str) -> BookSavedSchema:
        return


class MongoStorage(BaseStorage):
    def __init__(self):
        client = MongoClient(settings.URI)
        database = client[settings.SHOP_NAME_DB]
        self.collection = database[settings.BOOKS_COLLECTION]

    def get_book(self, book_id: str | ObjectId) -> BookSavedSchema:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(
                detail=f"Invalid book id '{book_id}'",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        query = {
             '_id': ObjectId(book_id)
        }
        raw_book = self.collection.find_one(query)
        if not raw_book:
            raise HTTPException(
                detail=f"Book with id '{book_id}' not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        book = BookSavedSchema(
            id=str(raw_book['_id']),
            **raw_book
        )
        return book

    def create_book(self, book: BookCreateSchema) -> BookSavedSchema:
        book_dict = book.model_dump()
        book_dict['created_at'] = datetime.now()

        result = self.collection.insert_one(document=book_dict)
        book_id = result.inserted_id
        # print(book_id)
        # saved = BookSavedSchema(
        #     id=str(book_id),
        #     **book_dict
        # )
        saved = self.get_book(book_id)
        return saved


storage: BaseStorage = MongoStorage()



#
# # READ
# # query = {
# #      '_id': ObjectId('6a47e78801643a4020beee0f')
# # }
# # first_book = collection.find_one(query)
# # print(first_book)
#
# query = {
#     # "title": "10 negro",
#     # 'price': 345,
#     # 'price': {'$gt': 340}
#     # 'price': {'$gte': 340}
#     # 'price': {'$lt': 341}
#     # 'price': {'$lte': 341}
#     # 'price': {'$lte': 341}
#     # 'price': {'$ne': 345}
#     # 'title': {'$regex': 'laptop lenovo', "$options": "i"}
#
#
#     '$and': [
#     # '$or': [
#             {'title': {'$regex': 'lenovo', "$options": "i"}},
#             {'title': {'$regex': 'laptop', "$options": "i"}},
#         ]
#     }
#
#
# books = collection.find(query).limit(6).sort('price', -1)#.skip(1)
# # print(books)
# # for book in books:
# #     print(book)
#
#
# # UPDATE#
# query = {
#     # '_id': ObjectId('6a47e78801643a4020beee0f')
# }
# new_data = {
#     # '$set': {'is_new': True}
#     # '$inc': {'price': -0.8}
#     '$mul': {'price': 1.2}
# }
# # collection.update_one()
# # result = collection.update_many(query, new_data)
# # print(result)
#
# # delete
# query = {
#     '_id': ObjectId('6a47e78801643a4020beee0f')
# }
# result = collection.delete_one(query)
# print(result)