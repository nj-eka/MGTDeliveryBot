FROM python:3.11-slim
RUN groupadd --gid 1000 node \
  && useradd --uid 1000 --gid node --shell /bin/bash --create-home node 
WORKDIR /home/node/app
COPY requirements.txt requirements.txt
RUN python3 -m pip install -U --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p 'log'
ENV TZ='Europe/Moscow'
ENV TG_BOT_LOG='/home/node/app/log'
CMD [ "python3", "main.py"]
