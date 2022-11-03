# finance_control

## how to run project

- run `pip install poetry`
- run `poetry install`
- run `cd ./src`
- run `alembic upgrade head`
- run `uvicorn src.app.main:app --host 127.0.0.1 --port 8000`