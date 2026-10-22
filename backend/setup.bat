REM setup venv
py -m venv .venv

REM start app
uvicorn app.main:app

REM init alembic
alembic init -t async migrations
