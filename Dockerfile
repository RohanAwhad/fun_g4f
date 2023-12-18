FROM python:3.11.6-slim-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt
RUN playwright install chromium

COPY main.py /app/main.py

CMD [ "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]