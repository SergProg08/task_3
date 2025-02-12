FROM python:3.11
LABEL authors="SergProd08"

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip

COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_3.wsgi:application"]