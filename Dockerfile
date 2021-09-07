FROM python:3

WORKDIR /usr/src/app

COPY req.txt ./

RUN pip install --no-cache-dir -r req.txt

RUN pip install gunicorn

COPY . .

CMD [ "gunicorn", "--bind=0.0.0.0", "--ca-certs=chain.pem", "--certfile=cert.pem", "--keyfile=privkey.pem", "app:app" ]




