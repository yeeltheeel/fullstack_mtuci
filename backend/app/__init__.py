from fastapi import FastAPI
from app.api import auth, user

def create_app() -> FastAPI:
    app = FastAPI(title="BookExchange API", version="0.1.0")

    app.include_router(auth.router)
    app.include_router(user.router)

    @app.get("/health", tags=["meta"])
    async def health():
        return {"status": "ok"}

    return app