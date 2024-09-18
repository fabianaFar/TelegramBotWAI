from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import logging
import database
from message import Message
from llama_cpp import Llama
import nest_asyncio
import json

nest_asyncio.apply()
messaggi = Message()
# Configura il logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#File config per ricavare il token
with open('config.json') as config_file:
    config = json.load(config_file)

# Configura il bot
TOKEN = config['TOKEN'] #Token del bot

model_name = "./modello/Mistral-7B-Instruct-v0.3-Q5_K_M.gguf"

# Carica il modello LLaMA
llm = Llama(
    model_path=model_name,
    n_gpu_layers=30,
    seed=1337,
    n_ctx=4096,
    chat_format="llama-2"
)

# Funzione che si attiva allo /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    username= user.username
    chat_id = update.effective_chat.id
    user_id = database.get_chat_id(chat_id)
    
    if user_id is None:
        # Se l'utente non esiste, lo inserisco nel database
        database.set_chat_id(chat_id)
        logger.info(f"Nuovo chat_id inserito: {chat_id}")
        text = "Benvenuto " + username + ". "
    else:
        logger.info(f"Utente esistente con chat_id: {chat_id}")
        text = "Bentornato "+ username + ". "
    
    keyboard = [
        [InlineKeyboardButton("Java ☕", callback_data="Java")],
        [InlineKeyboardButton("JavaScript 🟨", callback_data="JavaScript")],
        [InlineKeyboardButton("Python 🐍", callback_data="Python")],
        [InlineKeyboardButton("Cancella tutto", callback_data="delete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        text + await messaggi.get_messaggio("benvenuto"),
        reply_markup=reply_markup
    )

# Funzione che gestisce la scelta dei button
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = update.effective_chat.id

    language = query.data
    if (language != "delete"):
        keyboard = [
            [InlineKeyboardButton("Base", callback_data=f"{language}_Base")],
            [InlineKeyboardButton("Intermedio", callback_data=f"{language}_Intermedio")],
            [InlineKeyboardButton("Avanzato", callback_data=f"{language}_Avanzato")],
            [InlineKeyboardButton("Torna indietro", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Modifica il messaggio esistente con i nuovi bottoni
        await query.edit_message_text(
            await messaggi.get_messaggio("scelta", language),
            reply_markup=reply_markup
        )
    else:
        database.delete_id_utente(chat_id=chat_id)
        logger.info("Utente eliminato")
        await query.edit_message_text("Va bene, puoi ricominciare in qualsiasi momento digitando /start!")




async def handle_challenge(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    choice = query.data
    language, difficulty = choice.split('_') if '_' in choice else (None, None)
    logger.info(f"Query data: {choice}")
    

    if choice == "back":
        await start(update, context)
        return

    contexts = [{
    "role": "user",
    "content": (
            f"""Crea una sfida di coding sempre diversa e variegata da quella precedente. La sfida deve riguardare un problema di programmazione da risolvere in {language} con difficoltà {difficulty}. Segui questi requisiti rigorosamente:
            - Non includere mai codice, esempi di input/output o soluzioni, neanche implicitamente.
            - Titolo: Deve essere breve, descrittivo, e racchiuso tra tre asterischi (***).
            - Descrizione: Usa la parola 'Descrizione' per introdurre una spiegazione chiara e concisa del problema da risolvere. Non limitarti a problemi semplici come calcolatori o array.
            - La tematica delle sfide deve variare ampiamente: esplora problemi che includano interazione con API, database, algoritmi complessi, strutture di dati avanzate (come alberi o grafi), ottimizzazione o integrazione con tecnologie reali.
            - Evita la ripetizione delle stesse tematiche: diversifica le sfide includendo problemi reali e applicazioni concrete (come la gestione di file, comunicazione tra server, o strumenti di analisi dati).
            - Suggerimento: Fornisci un singolo suggerimento utile racchiuso tra asterischi (***), senza rivelare dettagli che potrebbero svelare la soluzione.
            - Limita la lunghezza totale della sfida a un massimo di 350 parole, mantenendo sempre una formulazione chiara e precisa.
            """

    )
}]


    text_random = await messaggi.random_message()
    keyboard = [
        [InlineKeyboardButton("Cambia challenge", callback_data="change")],
        [InlineKeyboardButton("Soluzione", callback_data="solution")],
        [InlineKeyboardButton("Ricomincia", callback_data="restart")],
        [InlineKeyboardButton("Termina", callback_data="stop")]
    ]
    replaymarkup= InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text= text_random)
    try:
        logger.info(contexts
                    )
        challenge = llm.create_chat_completion(messages=contexts, max_tokens=350)
        logger.info("Generato il contenuto della sfida")

        if challenge:
            challenge_content = challenge["choices"][0]["message"]["content"]
            chat_id = update.effective_chat.id

            # Verifica se la sfida è già presente per l'utente
            max_attempts = 5
            attempts = 0

            while database.get_challenge(chat_id, challenge_content) > 0 and attempts < max_attempts:
                logger.info("La sfida esiste già, genero una nuova sfida")
                challenge = llm.create_chat_completion(messages=contexts, max_tokens=350)
                if challenge:
                    challenge_content = challenge["choices"][0]["message"]["content"]
                    attempts += 1
                else:
                    keyboard.remove([1])
                    await query.edit_message_text(messaggi.get_messaggio("error"), reply_markup=replaymarkup)
                    return

            if attempts >= max_attempts:
                await query.edit_message_text("Non sono riuscito a generare una sfida unica. Per favore riprova più tardi.")
                return

            # Salva la nuova sfida nel database
            database.set_challenge(challenge_content, chat_id)
            logger.info(challenge_content)
            await query.edit_message_text(text=challenge_content, reply_markup=replaymarkup)
        else:
            await query.edit_message_text(messaggi.get_messaggio("error"))
    except Exception as e:
        keyboard.remove([1])
        await query.edit_message_text(messaggi.get_messaggio("error"), reply_markup=replaymarkup)
        logger.error(f"Errore nella generazione della sfida: {e}")

async def after_challenge (update: Update, context: CallbackContext):
    user = update.message.from_user
    username= user.username
    query = update.callback_query
    choise = query.data

    if(choise == "change"):
        await handle_challenge(update, context)
        return
    # elif(choise =="solution"):
    #     await generate_solution()
    #     return
    elif(choise =="restart"):
        await start()
        return
    elif (choise =="stop"):
        
        await query.edit_message_text(await messaggi.get_messaggio("saluti", username))
        return
    else:
        await query.edit_message_text("non mi è chiara la tua richiesta")

# async def generate_solution(update: Update, context: CallbackContext):
#     query = update.callback_query

#     challenge_content = database.get_last_challenge(update.effective_chat.id)  # Recupera l'ultima sfida dal DB
#     if not challenge_content:
#         await query.edit_message_text("Nessuna sfida trovata per generare la soluzione.")
#         return

#     messages = [{
#         "role": "user",
#         "content": f"Forniscimi la soluzione per la seguente sfida: {challenge_content}"
#     }]

#     try:
#         # Richiesta della soluzione tramite LLM
#         solution = llm.create_chat_completion(messages=messages, max_tokens=350)
#         solution_content = solution["choices"][0]["message"]["content"]
#         await query.edit_message_text(f"Soluzione: {solution_content}")
#     except Exception as e:
#         await query.edit_message_text("Generazione della soluzione non andata a buon fine")
#         logger.error(f"Errore nella generazione della soluzione: {e}")


async def echo(update: Update, context: CallbackContext) -> None:#Genera una sfida di coding per il linguaggio {language} con difficoltà {difficulty}. 
    await update.message.reply_text(update.message.text)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^(JavaScript|Python|Java|delete)$'))
    application.add_handler(CallbackQueryHandler(after_challenge, pattern='^(change|solution|restart|stop)$'))
    application.add_handler(CallbackQueryHandler(handle_challenge, pattern='^(JavaScript|Python|Java)_(Base|Intermedio|Avanzato|back)$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
