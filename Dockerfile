FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY update_dns.py helpers.py ./

CMD [ "python", "update_dns.py" ]