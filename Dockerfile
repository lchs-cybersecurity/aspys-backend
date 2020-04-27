# Production Dockerfile

FROM ubuntu
WORKDIR .
COPY . .

RUN cp config.example.json config.json
RUN apt update && apt install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 443

CMD ["/usr/bin/python3", "main.py"]
