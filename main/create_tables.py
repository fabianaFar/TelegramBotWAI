import json
from sqlalchemy import create_engine, Column, BigInteger, String, ForeignKey, DateTime, text  
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
import logging

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
else:
    logging.info(f"Connessione al database: {DATABASE_URL}")

# Definisci i modelli e crea le tabelle
Base = declarative_base()

class Utente(Base):
    __tablename__ = 'utenti'
    id_utente = Column(BigInteger, primary_key=True, index=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    
    # Relazione con le sfide
    challenges = relationship('Challenge', back_populates='utente', cascade='all, delete-orphan')

class Challenge(Base):
    __tablename__ = 'challenge'
    id_challenge = Column(BigInteger, primary_key=True, index=True)
    challenge = Column(String, nullable=False)
    chat_id_utente = Column(BigInteger, ForeignKey('utenti.chat_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("NOW()"))

    # Relazione con la tabella utenti
    utente = relationship('Utente', back_populates='challenges')

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
