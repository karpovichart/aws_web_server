FROM ubuntu:18.04
RUN apt update -y && apt install curl unzip python3 python3-pip libpq-dev -y && pip3 install psycopg2 && pip3 install flask && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install && rm awscliv2.zip
COPY . .
EXPOSE 8080