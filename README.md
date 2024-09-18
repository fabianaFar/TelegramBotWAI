### ITALIANO
# TelegramBotAI
TelegramBot with AI 

## Descrizione
Questo progetto è un bot Telegram che utilizza un modello di intelligenza artificiale per generare sfide di coding sui linguaggi quali Java, JS e Python. Il bot si connette a un database PostgreSQL per gestire le sfide e gli utenti.

## Prerequisiti
- Docker e Docker Compose installati.
- Un account Hugging Face per scaricare il modello.


## Configurazione del Modello
Il modello di grandi dimensioni utilizzato nel progetto non è incluso direttamente nella repository GitHub a causa delle limitazioni di dimensione dei file. Per ottenere il modello, utilizza il link qui sotto per scaricarlo da Hugging Face:

(Scarica il modello) (https://huggingface.co/jacobcarajo/Mistral-7B-Instruct-v0.3-Q5_K_M-GGUF/tree/main)
Una volta scaricato, inserisci il file del modello nella cartella `modello/` del progetto. Assicurati di aggiornare la variabile `model_name` nel codice sorgente con il nome del file del modello.


## Configurazione del Database

1. **Crea il Database:**
   Prima di avviare il bot, devi creare il database `telegram_bot` nel tuo server PostgreSQL. Puoi farlo utilizzando un client PostgreSQL come `psql` o strumenti come pgAdmin.
       ```sql
   CREATE DATABASE telegram_bot;



### ENGLISH

# TelegramBotAI
TelegramBot with AI

## Description
This project is a Telegram bot that uses a large-scale model to generate coding challenges on languages as Java, JS and Python. The bot connects to a PostgreSQL database to manage challenges and users.

## Prerequisites
- Docker and Docker Compose installed.
- A Hugging Face account to download the model.

## Model Configuration
The large-scale model used in this project is not included directly in the GitHub repository due to file size limitations. To obtain the model, use the link below to download it from Hugging Face:

(Download the model) (https://huggingface.co/jacobcarajo/Mistral-7B-Instruct-v0.3-Q5_K_M-GGUF/tree/main)
Once downloaded, place the model file in the `modello/` directory of the project. Make sure to update the `MODEL_NAME` constant in the source code with the name of the model file.

## Database Configuration
1. **Create the Database:**
   Before starting the bot, you need to create the `telegram_bot` database on your PostgreSQL server. You can do this using a PostgreSQL client like `psql` or tools like pgAdmin.
       ```sql
   CREATE DATABASE telegram_bot;