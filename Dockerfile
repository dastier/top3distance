FROM python:3.8.0-slim-buster

LABEL Author="Aliaksei Piatrouski"

WORKDIR /top3distances

COPY top3distances /top3distances

RUN python3 -m pip install psycopg2-binary

CMD ["python3", "populate_db.py"]