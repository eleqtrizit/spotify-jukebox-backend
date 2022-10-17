# pull official base image
FROM python:3.10-alpine

# set working directory within container
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir -p /tmp/partyatmyhouse

CMD ["sh", "start_production.sh"]
EXPOSE 8000/tcp
