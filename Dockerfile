FROM python:3.12.5

COPY main /bot/main/
COPY modello /bot/modello/
COPY main/font bot/main/font
COPY requirements.txt /bot/
RUN pip install -r /bot/requirements.txt && pip freeze
WORKDIR /bot/main
EXPOSE 5000

CMD ["sh", "-c", "python create_tables.py && python bot.py"]
