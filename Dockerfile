FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY run.sh .
RUN chmod +x run.sh

CMD ["./run.sh"]
