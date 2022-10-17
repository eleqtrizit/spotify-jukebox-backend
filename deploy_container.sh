#!/bin/sh

CID=$(docker container ls | cut -d' ' -f 1 | tail -n 1)
echo Building new container...
docker build -t spotify-jukebox-backend .

echo Stopping previous container...
docker stop $CID

echo Starting new container...
docker run -d --rm -p 8000:8000 spotify-jukebox-backend
