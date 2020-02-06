FROM ubuntu
WORKDIR .
COPY . .

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["/usr/bin/python3", "main.py"]