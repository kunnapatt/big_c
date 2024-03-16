FROM python:3.9

ENV PORT=8000
ENV WEBSITE=website_a

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r ./requirements.txt

COPY . .

CMD exec uvicorn api:app --host 0.0.0.0 --port $PORT