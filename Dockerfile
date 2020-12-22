FROM bitnami/python:3.7.9

ENV type authors
WORKDIR /crawler

RUN apt-get update -y && \
    apt-get install -y tor

COPY . .
RUN pip install -r requirements.txt

CMD ./setup_tor.sh
CMD python3 main.py $type
CMD ["sh", "-c", " python3 main.py ${type}"]
