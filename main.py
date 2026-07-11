from fastapi import FastAPI
from api_router import api_router


app = FastAPI(
    title='Book store',
    version='2'
)

app.include_router(api_router, tags=['Books'])