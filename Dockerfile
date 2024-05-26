FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

ENV FLASK_APP=app.py

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
