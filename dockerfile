FROM python:3.9

ENV PYTHONUNBUFFERED True
ENV PORT 5000

WORKDIR /ml-api

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install google-cloud-storage

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host", "0.0.0.0" ]