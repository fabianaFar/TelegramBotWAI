import json
import os
from sqlalchemy import create_engine, Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError

# Carica la configurazione dal file config.json
def load_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        return json.load(file)

# Carica la configurazione
config = load_config()

# Recupera l'URL del database e altre variabili di configurazione
DATABASE_URL = config.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL non trovato nel file di configurazione.")

# Definisci i modelli e crea le tabelle
Base = declarative_base()

class Utente(Base):
    __tablename__ = 'utenti'
    id_utente = Column(BigInteger, primary_key=True, index=True)
    chat_id = Column(String, unique=True, nullable=False)

class Challenge(Base):
    __tablename__ = 'challenge'
    id_challenge = Column(BigInteger, primary_key=True, index=True)
    challenge = Column(String, nullable=False)
    chat_id_utente = Column(BigInteger, ForeignKey('utenti.id_utente'))

    # Relazione con la tabella utenti
    utente = relationship('Utente')

# Configura la connessione al database
engine = create_engine(DATABASE_URL)

def create_tables():
    try:
        Base.metadata.create_all(engine)
        print("Tabelle create con successo.")
    except SQLAlchemyError as e:
        print(f"Errore nella creazione delle tabelle: {e}")

if __name__ == '__main__':
    create_tables()
