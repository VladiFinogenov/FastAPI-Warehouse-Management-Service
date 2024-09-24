from fastapi import FastAPI
from app.api.routes import products, orders
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Warehouse Management Service"}


app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
