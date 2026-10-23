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

@REM  REM start db
@REM  docker desktop start
@REM  cd ..
@REM  docker compose up -d

REM start app
uvicorn app.main:app --reload

@REM  REM finish
@REM  docker compose down
@REM  docker desktop stop
