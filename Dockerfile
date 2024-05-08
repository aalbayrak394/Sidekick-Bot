FROM python:3

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]