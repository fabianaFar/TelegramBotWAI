from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import logging
import database as database
from message import Message
from llama_cpp import Llama
from pdf_generator import PDF
import nest_asyncio
import json

nest_asyncio.apply()
messaggi = Message()

# Configura il logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#File config per ricavare il token e model_name
with open('config.json') as config_file:
    config = json.load(config_file)

# Configura il bot
TOKEN = config['TOKEN'] #Token del bot
model_name = config['model_name'] #model AI 

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
       # Verifica se è un comando (/start) o una CallbackQuery
    if update.message:
        user = update.message.from_user
        chat_id = update.message.chat_id
        query = None
    elif update.callback_query:
        user = update.callback_query.from_user
        chat_id = update.callback_query.message.chat_id
        query = update.callback_query  # Definisci 'query' solo in caso di CallbackQuery
    else:
        logger.error("Impossibile determinare l'utente e il chat_id.")
        return

    username = user.username
    user_id = database.get_chat_id(chat_id)

    logger.info(f"Chat ID: {chat_id}, Username: {username}")
    
    # Memorizza chat_id e username in una variabile di sessione
    context.user_data['chat_id'] = chat_id
    context.user_data['username'] = username


    #Set dei button da mostrare all'invio del messaggio
    keyboard = [
        [InlineKeyboardButton("Java ☕", callback_data="Java")],
        [InlineKeyboardButton("JavaScript 🟨", callback_data="JavaScript")],
        [InlineKeyboardButton("Python 🐍", callback_data="Python")],
    ]
    #Button aggiuntivo in caso in cui l'utente è già registrato
    keyboard_not_new_user = [[InlineKeyboardButton("Elimina Cronologia", callback_data="delete")]]
    
    #racchiudo in una variabile i button
    reply_markup = InlineKeyboardMarkup(keyboard)

    choise = query.data if query and query.data else None

    
    if choise is None or "back" not in choise:
     # Se l'utente non esiste, lo inserisco nel database
        if user_id is None:
            database.set_chat_id(chat_id)
            final_text= await messaggi.get_messaggio("benvenuto", username)
        #Altrimenti:
        else:
            final_text = await messaggi.get_messaggio("bentornato", username)
            keyboard.extend(keyboard_not_new_user)
            reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        final_text = await messaggi.get_messaggio("return")
        reply_markup = InlineKeyboardMarkup(keyboard)


    #Invio il messaggio
    if update.message:
        await update.message.reply_text(final_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(final_text, reply_markup=reply_markup)


# Funzione che gestisce la scelta dei button
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = update.effective_chat.id
    language = query.data

    if language != "delete":
        keyboard = [
            [InlineKeyboardButton("Base", callback_data=f"{language}_Base")],
            [InlineKeyboardButton("Intermedio", callback_data=f"{language}_Intermedio")],
            [InlineKeyboardButton("Avanzato", callback_data=f"{language}_Avanzato")],
            [InlineKeyboardButton("Torna indietro", callback_data=f"{language}_back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Modifica il messaggio esistente con i nuovi bottoni per la scelta della difficoltà
        await query.edit_message_text(
            await messaggi.get_messaggio("scelta", language),
            reply_markup=reply_markup
        )
    # Se l'utente vuole eliminare la cronologia
    elif language == "delete":
        database.delete_id_utente(chat_id=chat_id)
        await query.edit_message_text(await messaggi.get_messaggio("ricomincia"))
    



async def handle_challenge(update: Update, context: CallbackContext) -> None:
    query = update.callback_query if update.callback_query else None
    choice = query.data
    language, difficulty = choice.split('_') if '_' in choice else (None, None)
    logger.info(f"Query data: {choice}")
    

    if difficulty == "back":
            await start(update, context)
            return

    #Richiesta al modello AI
    contexts = [{
    "role": "user",
    "content": (
            f"""Crea una sfida di coding sempre diversa e variegata da quella precedente. La sfida deve riguardare un problema di programmazione da risolvere in {language} con difficoltà {difficulty}. Segui questi requisiti rigorosamente:
            - Non includere mai codice, esempi di input/output o soluzioni, neanche implicitamente.
            - Titolo: Deve essere breve, descrittivo, e racchiuso tra tre asterischi, precisando il linguaggio scelto dall'utente (***).
            - Descrizione: Usa la parola 'Descrizione' per introdurre una spiegazione chiara e concisa del problema da risolvere. Non limitarti a problemi semplici come calcolatori o array.
            - La tematica delle sfide deve variare ampiamente: esplora problemi che includano interazione con API, database, algoritmi complessi, strutture di dati avanzate (come alberi o grafi), ottimizzazione o integrazione con tecnologie reali.
            - Evita la ripetizione delle stesse tematiche: diversifica le sfide includendo problemi reali e applicazioni concrete (come la gestione di file, comunicazione tra server, o    strumenti di analisi dati).
            - Suggerimento: Fornisci un singolo suggerimento utile racchiuso tra asterischi (***), senza rivelare dettagli che potrebbero svelare la soluzione.
            - Non ripetere le sfide, non proporre sempre sfide con database di libri.
            - Limita la lunghezza totale della sfida a un massimo di 350 parole, mantenendo sempre una formulazione chiara e precisa.
            """

    )
}]
    text_random = await messaggi.random_message() #recupera i messaggi in maniera randomica dalla classe Messaggi (message.py)
    keyboard = [
        [InlineKeyboardButton("Cambia challenge", callback_data="change")],
        [InlineKeyboardButton("Soluzione", callback_data="solution")],
        [InlineKeyboardButton("Ricomincia", callback_data="restart")],
        [InlineKeyboardButton("Termina", callback_data="stop")]
    ]
    replaymarkup= InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text= text_random)
    try:
        challenge = llm.create_chat_completion(messages=contexts, max_tokens=350)
        if challenge:
            challenge_content = challenge["choices"][0]["message"]["content"]
            chat_id = update.effective_chat.id

            # Verifica se la sfida è già presente per l'utente
            max_attempts = 5 #massimo dei tentativi per la generazione di sfide
            attempts = 0 #tentativi attuali
            
            #Controlla se la challenge è stata già generata e ne genera una nuova
            while database.get_challenge(chat_id, challenge_content) > 0 and attempts < max_attempts:
                challenge = llm.create_chat_completion(messages=contexts, max_tokens=350)
                if challenge:
                    challenge_content = challenge["choices"][0]["message"]["content"]
                    attempts += 1 #aumenta di uno i tentativi
                else:
                    keyboard.remove([1]) #in caso di errore
                    await query.edit_message_text(await messaggi.get_messaggio("error"), reply_markup=replaymarkup)
                    return
            #se i tentativi superano i 5
            if attempts >= max_attempts:
                keyboard.remove([1])
                await query.edit_message_text("Non sono riuscito a generare una sfida unica. Per favore riprova più tardi.", reply_markup=replaymarkup)
                return

            # Se tutto va bene allora salva la nuova sfida nel database
            database.set_challenge(challenge_content, chat_id)
            await query.edit_message_text(text=challenge_content, reply_markup=replaymarkup)
        else:
            await query.edit_message_text(messaggi.get_messaggio("error"))
    except Exception as e:
        keyboard.remove([1])
        await query.edit_message_text(messaggi.get_messaggio("error"), reply_markup=replaymarkup)
        logger.error(f"Errore nella generazione della sfida: {e}")

    
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def solution(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = update.effective_chat.id
    recupered_challenge = database.get_last_challenge(chat_id=chat_id)
    contexts = [{
        "role": "user",
        "content": (
            f"""Trova una soluzione per questa sfida {recupered_challenge} in codice di programmazione, aggiungendo qualche commento descrittivo che spieghi il codice.
              La soluzione deve avere sempre una formulazione chiara e precisa.
              Ricorda di rispettare il linguaggio utilizzato per la challenge.
            """
        )
    }]
    
    keyboard = [
        [InlineKeyboardButton("Ricomincia", callback_data="restart")],
        [InlineKeyboardButton("Termina", callback_data="stop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    random_solution = await messaggi.random_solution_message()
    # Messaggio di attesa per l'utente
    await query.edit_message_text(text=random_solution)

    try:
        # Chiamata all'intelligenza artificiale per generare la soluzione
        challenge = llm.create_chat_completion(messages=contexts)
        if challenge:
            challenge_content = challenge["choices"][0]["message"]["content"]
            logger.info(challenge_content)
            # Genera il PDF con la risposta dell'AI
            pdf = PDF()
            pdf.generate_pdf(challenge_content, "solution.pdf")

            # Invia il PDF in chat
            await context.bot.send_document(chat_id=chat_id, document=open("solution.pdf", "rb"))

            # Rimuovi il file PDF dopo l'invio per evitare accumulo di file
            os.remove("solution.pdf")

            # Invia il messaggio di testo con la soluzione
            await query.edit_message_text(text="Ecco la soluzione generata:")
            await context.bot.send_message(chat_id=chat_id, text="Puoi scegliere se proseguire o terminare: ", reply_markup=reply_markup)
            return
        else:
            await query.edit_message_text("Non sono riuscito a generare la soluzione, mi spiace.")
            return
    except Exception as e:
        logger.error(f"Errore nella generazione della soluzione: {e}")
        await query.edit_message_text("Si è verificato un errore durante la generazione della soluzione.")
        return


async def after_challenge (update: Update, context: CallbackContext):
    query = update.callback_query
    choise = query.data
    

    if(choise == "change"):
        await handle_challenge(update, context)
        return
    elif (choise == "solution"):
        await solution(update, context)
        return
    elif(choise == "stop"):
        text= await messaggi.get_messaggio("saluti")
        await query.edit_message_text(text=text)
        return
    elif (choise == "restart"):
        await start(update, context)
        return
    else:
        await query.edit_message_text("non mi è chiara la tua richiesta")


async def echo(update: Update, context: CallbackContext) -> None:
    random_msg = await messaggi.user_typing()
    await update.message.reply_text(text=random_msg)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^(JavaScript|Python|Java|delete)$'))
    application.add_handler(CallbackQueryHandler(handle_challenge, pattern='^(JavaScript|Python|Java)_(Base|Intermedio|Avanzato|back)$'))
    application.add_handler(CallbackQueryHandler(after_challenge, pattern='^(change|solution|restart|stop)$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
