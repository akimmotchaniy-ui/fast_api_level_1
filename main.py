from fastapi import FastAPI
from api_router import api_router


app = FastAPI(
    title='Travel Agency',
    version='1',
)

app.include_router(api_router, tags=['Tours'])
