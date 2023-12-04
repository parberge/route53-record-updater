FROM python:3.12-alpine

WORKDIR /usr/src/app

RUN pip install micropipenv
COPY Pipfile.lock Pipfile ./
RUN micropipenv install

COPY update_dns.py helpers.py ./

CMD [ "python", "update_dns.py" ]