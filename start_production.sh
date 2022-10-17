#!/bin/sh

# uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
gunicorn main:app -b 0.0.0.0 -w 8 -k uvicorn.workers.UvicornWorker
