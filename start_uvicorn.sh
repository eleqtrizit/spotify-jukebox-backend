#!/bin/sh

# uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
gunicorn main:app --port 8000 -w 32 -k uvicorn.workers.UvicornWorker
