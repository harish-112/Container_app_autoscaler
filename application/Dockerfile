FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN pip install --no-cache-dir fastapi uvicorn

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]