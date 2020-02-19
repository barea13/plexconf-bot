FROM python:3.7-slim

COPY requeriments.txt /

RUN pip install --no-cache-dir -r /requeriments.txt

COPY . /app/
WORKDIR /app

CMD python bot.py