FROM python:3.11

WORKDIR /app

COPY requrements.txt /app

COPY src /app

RUN pip install -r requriments.txt

CMD ["python","main.py"]