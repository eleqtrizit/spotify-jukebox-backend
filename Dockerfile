# pull official base image
FROM python:3.10-alpine

# set working directory within container
WORKDIR /app
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["sh", "start_production.sh"]
EXPOSE 8000/tcp
