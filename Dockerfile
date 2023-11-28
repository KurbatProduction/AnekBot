FROM python:3.11-alpine
RUN apk add --no-cache py3-pip

WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt

CMD ["python3", "app.py"]