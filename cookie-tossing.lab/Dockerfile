FROM python:3.10-alpine3.17-241022

WORKDIR /app

COPY . .
RUN pip install flask

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0"] 