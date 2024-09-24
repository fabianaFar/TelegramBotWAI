import random
from typing import List, Optional

class Message:
    def __init__(self):
        self.messaggi = {
            "benvenuto": "Benvenuto {}! \nSei nel canale di coding test di ✨ Unitiva!✨ 🥳 \nQui potrai mettere alla prova le tue competenze attraverso delle divertenti sfide di coding!🤖💻 \nPer cominciare, quale linguaggio vuoi scegliere?⤵️",
            "bentornato" : "Bentornato {}! \nRieccoti nel nostro canale, è bello rivederti.🤩\nLe sfide che hai già sostenuto sono state immagazzinate in memoria per garantirti un'esperienza unica e non ripetitiva, pertanto se desideri rimuovere i salvataggi ti basterà cliccare su 'Ripristina cronologia'.😉\nChe sfida vuoi sostenere oggi?⤵️",
            "scelta": "😎Perfetto!😎 Hai scelto {} 😏! Ora non ti resta che scegliere il livello di difficoltà:",
            "delete_history": "Va bene, puoi ricominciare in qualsiasi momento digitando /start!",
            "error" : "Generazione non andata a buon fine",
            "saluti": "E' stato un piacere averti con noi! Spero che questo canale ti abbia permesso di prepararti al meglio. Noi saremo qui quando ne avrai bisogno!😉 A presto!💪",
            "ricomincia": "Hai deciso di eliminare tutta la cronologia, per cui non sono più presenti sfide associate al tuo user! Puoi ricominciare da capo in qualsiasi momento, ti basta digitare /start!",
            "return" : "Pare che tu abbia cambiato idea sul linguaggio che hai scelto 😏. \nPuoi riselezionarlo: ⤵️"
        }
    async def get_messaggio(self, chiave: str, valore: Optional[str] = None) -> str:
        if valore is not None:
            return self.messaggi.get(chiave, "Chiave non valida").format(valore)
        return self.messaggi.get(chiave, "Chiave non valida")

    async def random_message(self) -> str:
        text_generation_challenge: List[str] = [
            "Generazione in corso, potrebbe volerci qualche minuto, abbi un po' di pazienza...🔄",
            "Stiamo preparando la tua sfida... Nel frattempo, perché non pensi al tuo superpotere di programmazione? 😉",
            "La tua risposta è in arrivo! Nel frattempo, prendi un caffè o fai stretching, è sempre una buona idea! ☕️🧘‍♀️",
            "Stiamo lavorando sulla tua richiesta! Perché non prendi un respiro profondo e immagina il codice perfetto? 🌬️💡",
            "La tua sfida sta per arrivare... Hai già pensato a come la risolverai? Nel frattempo, rilassati un attimo! 😌",
            "Risposta in arrivo! Nel frattempo, concediti un attimo di pausa o fai una danza della vittoria anticipata 💃🕺",
            "Abbiamo quasi finito! Intanto, sfida te stesso a pensare alla soluzione più creativa che potresti trovare! 💡",
            "La tua sfida è quasi pronta... perché non fai un rapido 'push-up' mentre aspetti? 💪",
            "Stiamo preparando la tua sfida... nel frattempo, pensa al tuo meme di programmazione preferito! 😄",
            "Risposta in corso... hai già pensato a quale editor di codice usare per affrontarla? ✨",
            "Siamo quasi pronti! Nel frattempo, perché non giochi a indovinare il tema della sfida? 🎯"
        ]

        return random.choice(text_generation_challenge)
    

    async def random_solution_message(self) -> str:
        text_generation_solution : List[str] = [
           "Stiamo facendo magia dietro le quinte! 🪄 Torniamo presto con la soluzione. Puoi metterti comodo nel mentre!", "I nostri ingegneri dei sogni stanno lavorando su questo! 🌟 Rimanete sintonizzati.",
           "Abbiamo messo il caffè in macchina e stiamo risolvendo il mistero! ☕️🚀", "In questo momento, siamo impegnati a risolvere il rompicapo. 🧩 Resta con noi!", "Il nostro team sta mettendo a punto la risposta perfetta. 🤓💡","Siamo al lavoro per rendere tutto perfetto. 🚧 Grazie per la pazienza!",  "Stiamo preparando la tua soluzione, come dei veri ninja del codice! 🥷💻", "Abbiamo acceso le luci del backstage e siamo in modalità risoluzione! 🎭💡", "Ci stiamo cimentando in una piccola magia informatica. 🎩✨ Torniamo presto con i risultati!","Siamo al lavoro e abbiamo preso il nostro kit di strumenti virtuali. 🛠️🔍 A breve la soluzione!"
        ]
        return random.choice(text_generation_solution)
    

    async def user_typing(self) -> str:
        random_answer: List[str] = [
            "Mhh, forse non ho ben capito cosa mi hai chiesto 😢​, puoi digitare /start per ricominciare oppure cliccare uno dei button per fare la tua scelta! 💡",
            "Hei hei 😅​ la mia intelligenza artificiale è solo per le sifde di coding.",
            "Mi spiace ma sono programmato solo per somministrare sfide, non per altre piacevoli conversazioni. 🤭​",
            "Ops, mi sai che hai eseguito un'azione per cui non sono programmato (non sono batman 🤌​)",
        ]

        return random.choices(random_answer)
