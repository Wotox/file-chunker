FROM python:3.12

WORKDIR /api

ADD . /api

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]