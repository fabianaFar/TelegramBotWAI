import random
from typing import List, Optional

class Message:
    def __init__(self):
        self.messaggi = {
            "benvenuto": "\nSei nel canale di coding test di ✨ Unitiva!✨ 🥳 \nQui potrai mettere alla prova le tue competenze attraverso delle divertenti sfide di coding!🤖💻 \nPer cominciare, quale linguaggio vuoi scegliere?⤵️",
            "scelta": "😎Perfetto!😎 Hai scelto {} 😏! Ora non ti resta che scegliere il livello di difficoltà:",
            "delete_history": "Va bene, puoi ricominciare in qualsiasi momento digitando /start!",
            "error" : "Generazione non andata a buon fine",
            "saluti": "E' stato un piacere averti con noi! Spero che questo canale ti abbia permesso di prepararti al meglio. Noi saremo qui quando ne avrai bisogno!😉 A presto!💪"
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
