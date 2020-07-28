FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV DB_ENDPOINT "52.255.160.180:8080"
ENV LISTEN_PORT 5001
ENV DB_NAME="chaos"

EXPOSE 5001
COPY ./app /app
RUN pip install -r requirements.txt
