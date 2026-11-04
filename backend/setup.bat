REM setup venv
py -m venv .venv
.venv/Scripts/Activate.ps1
pip install -r requirements.txt

REM init alembic
alembic init -t async migrations
alembic revision --autogenerate -m "init schema"
alembic upgrade head
alembic current

REM create db
py seed.py

REM start app
uvicorn app.main:app --reload

@REM start all
docker desktop start
docker compose up -d

@REM finish all
docker compose down -v
docker desktop stop
