FROM python:3.12-alpine

WORKDIR /app

COPY . .
COPY

RUN apk add --no-cache gcc musl-dev postgresql-dev

RUN pip install --upgrade pip
RUN pip install -r  requirements.txt

CMD ["python", "/app/run.py"]