from fastapi import FastAPI
from app.api import auth, users, books, locations, stock, bookings

def create_app() -> FastAPI:
    app = FastAPI(title="bookexchange api", version="0.1.0")

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(books.router)
    app.include_router(locations.router)
    app.include_router(stock.router)
    app.include_router(bookings.router)

    @app.get("/health", tags=["meta"])
    async def health():
        return {"status": "ok"}

    return app
