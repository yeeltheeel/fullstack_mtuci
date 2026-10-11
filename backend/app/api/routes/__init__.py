from fastapi import APIRouter
from . import users, books, locations, stock, bookings

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(books.router)
api_router.include_router(locations.router)
api_router.include_router(stock.router)
api_router.include_router(bookings.router)