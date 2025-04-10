FROM python:3.12

WORKDIR /app

COPY requirements/prod.txt .

RUN pip install -r prod.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]