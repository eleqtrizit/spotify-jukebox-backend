#!/bin/sh

kill -9 `pgrep -f uvicorn`
kill -9 `pgrep -f spawn_main`

