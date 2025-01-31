import enum
import logging
from typing import Union, Type

from visca.baseClasses.getClass import GetInterfaceClass

logging.basicConfig(level=logging.DEBUG)

class BaseInterfaceClass:

    """
    La classe BaseInterfaceClass fornisce un'interfaccia di base per avere
    i comandi da inviare alla camera e gestire le risposte che arrivano dalla camera.

    Quello che serve è una specie di super dizionario che
    in base al comando selezionato restituisca sotto forma di stringa il comando
    da inviare alla camera. Scrivendo ad esempio getExposureMode()
    ritorna il comando "09 04 00 02 00 FF". setExposureMode(0x02) ritorna "01 04 00 02 02 FF".

    Quando viene inviato un comando alla camera, ci si aspetta una risposta:

    - ACK: conferma che il comando è stato ricevuto la camera lo sta processando.
    - Completion: conferma che il comando è stato completato con successo.
    -Error: conferma che il comando non è stato completato con successo.

    Il valore viene memorizzato in una variabile solo se il comando è un set. Nel caso
    in cui il sistema risponda con in modo diverso da un completion, viene impostata
    su true la variabile _isUpdateRequired in modo da informare l'utente che è necessario
    un aggiornamento dell'interfaccia.

    Quando invece si ha un get, la risposta contiene il valore quindi la funzione handle_reply()
    farà il parsing della risposta e aggiornerà lo stato in base al comando più recente.
    """

    _isUpdateRequired = False  # Flag per indicare se l'interfaccia deve essere aggiornata
    _last_command = None
    command_map = {
        # example: "exposureMode": {"reply_format": "00 00 0p 0p", "placeholder": ["p"]}
    }
    command_to_state_map = {
        # example: "exposureMode": _exposureMode
    }
    defaultValue = {
        # example: "exposureMode": 0x00
    }

    getClass = None

    @property
    def last_command(self):
        return self._last_command

    def setup(self):
        """
        Imposta un valore nella camera.
        """
        self.getClass = GetInterfaceClass(self)


    def handle_reply(self, reply):
        """
        Gestisce la risposta dalla telecamera e aggiorna lo stato in base
        al comando più recente.

        La risposta è una tupla che contiene:
        - Il codice di risposta (50 per Completion, 40 per ACK, 60 per Error)
        - I valori opzionali restituiti dalla camera
        - quando viene fatto un get il valore è restituito come una stringa:
          ("50","04 39 01")
        """
        logging.debug(f"Risposta ricevuta: {reply}")
        if not self._last_command:
            logging.info("\n\tNessun comando precedente da gestire.")
            return

        # Assicurati che il codice sia una stringa coerente per il confronto
        response_code = int(reply[0])
        logging.debug(f"Ultimo comando: {self._last_command}")
        logging.debug(f"Codice risposta: {response_code}")

        # se riceve un ack allora vuol dire che il comando è stato ricevuto
        # ma non è stato processato
        if self.is_ack(response_code):
            logging.info(f"\n\tACK ricevuto : {reply} - Comando: {self._last_command}")
            self._isUpdateRequired = True  # Richiede un aggiornamento
            return

        # se riceve un completion allora vuol dire che il comando è stato processato
        if self.is_completion(response_code):
            logging.info(f"\n\tCompletion ricevuto : {reply} - Comando: {self._last_command}")
            return

        # se riceve un errore allora vuol dire che il comando non è stato processato
        if self.is_error(response_code):
            error_code = reply[1] if len(reply) > 1 else None
            logging.info(f"\n\tErrore ricevuto : {reply} - Comando: {self._last_command}")
            self.handle_error(error_code)
            self._last_command = None
            return

        logging.info(f"\n\tRisposta sconosciuta: {reply}")

    # --- Metodi di utilità ---

    @staticmethod
    def is_ack(response_code):
        return response_code == 40

    @staticmethod
    def is_completion(response_code):
        return response_code == 50

    @staticmethod
    def is_error(response_code):
        return response_code == 60

    @staticmethod
    def handle_error(error_code):
        """
        Gestisce gli errori in base al codice di errore.
        """
        error_messages = {
            1: "Comando non riconosciuto.",
            2: "Valore non valido.",
            3: "Comando non eseguibile nel contesto attuale.",
        }
        logging.info(f"\n\tErrore: {error_messages.get(error_code, 'Errore sconosciuto.')}")

    def process_completion(self, reply):
        """
        Aggiorna lo stato in base alla risposta Completion.
        """
        logging.debug(f"process completion: {reply[1:]}")
        if "get" in self._last_command:
            if self.getClass:
                self.getClass.onGetCommand(reply[1:])  # Passa i valori di ritorno
            else:
                logging.error("\n\tWARNING: Nessuna classe GET associata.")

    @staticmethod
    def getMaxValue(enum_or_list: Union[Type[enum.Enum], list[int]]) -> int:
        """
        Restituisce il valore massimo da un'enumerazione o lista di interi.
        :param enum_or_list: Enumerazione o lista di interi.
        :return: Valore massimo.
        """
        if isinstance(enum_or_list, list):
            return max(enum_or_list)
        elif issubclass(enum_or_list, enum.Enum):
            return max(e.value for e in enum_or_list)
        raise ValueError("Input deve essere un'enumerazione o una lista valida.")

    @staticmethod
    def getMinValue(enum_or_list: Union[Type[enum.Enum], list[int]]) -> int:
        """
        Restituisce il valore minimo da un'enumerazione o lista di interi.
        :param enum_or_list: Enumerazione o lista di interi.
        :return: Valore minimo.
        """
        if isinstance(enum_or_list, list):
            return min(enum_or_list)
        elif issubclass(enum_or_list, enum.Enum):
            return min(e.value for e in enum_or_list)
        raise ValueError("Input deve essere un'enumerazione o una lista valida.")