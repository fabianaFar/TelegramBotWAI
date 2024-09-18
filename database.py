import logging
import psycopg2
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:password@localhost:5432/telegram_bot"
logger = logging.getLogger(__name__)
# Gestione della connessione con un context manager
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        yield conn
    except Exception as e:
        logger.info(f"Errore durante la connessione al database: {e}")
        raise
    finally:
        if conn:
            conn.close()

# Funzione per ottenere l'id utente tramite chat_id
def get_chat_id(chat_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_utente FROM utenti WHERE chat_id = %s", (chat_id,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        logger.info(f"Errore durante la query: {e}")
        return None
    
    return result[0] if result else None

# Funzione per impostare un nuovo chat_id nel database
def set_chat_id(chat_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO utenti (chat_id) VALUES(%s)", (chat_id,))
            conn.commit()  # Importante per salvare le modifiche nel database
    except Exception as e:
        logger.info(f"Errore durante l'inserimento nel database: {e}")
    

def delete_id_utente(chat_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM utenti WHERE chat_id=%s"
            cursor.execute(query, (chat_id,))
            conn.commit()
            logger.info("Utente eliminato correttamente")
    except Exception as e:
        logger.error(f"Errore durante l'eliminazione dell'utente: {e}")

def get_challenge(chat_id, challenge):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM challenge WHERE chat_id_utente = %s AND challenge = %s", (chat_id, challenge))
            result = cursor.fetchone()[0]
            return result
    except Exception as e:
        logger.info("Problema nel recuperare la sfida")
        return 0

def set_challenge(challenge, chat_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO challenge (challenge, chat_id_utente) VALUES (%s, %s)", (challenge, chat_id))
            conn.commit()
    except Exception as e:
        logger.info("Errore nell'inserimento della sfida", e)