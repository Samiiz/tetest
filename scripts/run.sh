#!/bin/sh

aerich init -t app.configs.database_settings.TORTOISE_ORM

poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
