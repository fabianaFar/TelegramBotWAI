FROM python:3.12.5

COPY . /bot
WORKDIR /bot
RUN pip install -r requirements.txt 
EXPOSE 5000

CMD ["python", "bot.py"]