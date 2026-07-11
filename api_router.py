from fastapi import APIRouter, status

from schemas import BookCreateSchema, BookSavedSchema
from storage import storage

api_router = APIRouter(
    prefix='/api/books'
)


@api_router.get('')
def index_books():
    return 2222


@api_router.get('/{book_id}')
def get_book(book_id: str) -> BookSavedSchema:
    book = storage.get_book(book_id)
    return book


@api_router.post('', status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema) -> BookSavedSchema:
    """the single endpoint for creating book in storage"""
    created_book = storage.create_book(book)
    return created_book