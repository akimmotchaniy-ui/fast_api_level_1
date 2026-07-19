from fastapi import FastAPI
from api_router import api_router


app = FastAPI(
    title='Tour agency',
    version='1'
)

app.include_router(api_router, tags=['Tours'])
