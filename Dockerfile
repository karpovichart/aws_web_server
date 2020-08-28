FROM ubuntu:18.04
RUN apt update -y && apt install python3 -y && apt install python3-pip -y && apt install libpq-dev -y && pip3 install psycopg2
COPY . .
EXPOSE 8080
