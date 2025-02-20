FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn ATM_server.wsgi:application --bind 0.0.0.0:$PORT