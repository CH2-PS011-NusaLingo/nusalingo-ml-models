FROM python:3.9

WORKDIR /ml-api

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ]