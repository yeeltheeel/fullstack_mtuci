from fastapi import FastAPI
from app.api import auth, user, book, location, stock, booking

def create_app() -> FastAPI:
    app = FastAPI(title="bookexchange api", version="0.1.0")

    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(book.router)
    app.include_router(location.router)
    app.include_router(stock.router)
    app.include_router(booking.router)

    @app.get("/health", tags=["meta"])
    async def health():
        return {"status": "ok"}

    return app
