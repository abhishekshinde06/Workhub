FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip --default-timeout=300 --retries=10 install -r requirements.txt
COPY project_workhub/ .

ENV PYTHONPATH="/app/project_workhub"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  