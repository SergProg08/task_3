FROM python:3.11
LABEL authors="SergProg08"

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip install --upgrade pip

COPY  . /app/
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000"]