import logging
from enum import Enum


class GetInterfaceClass:

    def __init__(self, baseClass):
        self.baseClass = baseClass

    @property
    def command_map(self):
        return self.baseClass.command_map

    @property
    def defaultValue(self):
        return self.baseClass.defaultValue

    @property
    def _last_command(self):
        if not "_" in self.baseClass.last_command:
            raise ValueError(f"Ultimo comando non valido: {self.baseClass.last_command}")
        return self.baseClass.last_command

    def onGetCommand(self, reply):
        """
        Aggiorna lo stato interno in base alla risposta di un comando GET.
        """
        logging.debug(f"\n\tRisposta GET ricevuta: {reply} type: {type(reply)}")

        # Step 1: Recupera l'ultimo comando
        command = self._get_last_command()
        if not command:
            return

        # Step 2: Ottieni i dettagli del comando dal dizionario
        command_details = self._get_command_details(command)
        if not command_details:
            return

        # 2a la risposta contiene l'inquire command
        inquire = command_details.get("inquire")
        if inquire:
            logging.debug(f"\n\tInquire command: {inquire} - Risposta: {reply}")
            reply = reply[0].replace(inquire, "")
            logging.debug(f"\n\tRisposta modificata: {reply}")

        # Step 3: Parsing della risposta
        parsed_values = self.parse_response(reply, command_details)
        combined_value = self._combine_values(parsed_values, command_details.get("placeholder", []))

        # Step 4: Aggiorna la variabile di stato
        self._update_state(command, combined_value)

    def _get_last_command(self):
        """
        Determina il comando dall'ultimo comando inviato.
        """
        if not self._last_command:
            logging.error("\n\tNessun comando precedente da gestire.")
            return None
        logging.info(f"\n\tUltimo comando: {self._last_command}")
        last_command_parts = self._last_command.split(" ")
        logging.info(f"\n\tLast Command Parts: {last_command_parts}")
        if len(last_command_parts) < 2:
            logging.error(f"\n\tFormato del comando non valido: {self._last_command}")
            return None

        return last_command_parts[1]

    def _get_command_details(self, command):
        """
        Ottieni i dettagli del comando dal dizionario.
        """
        command_details = self.command_map.get(command)
        if not command_details:
            logging.error(f"\n\tComando GET non riconosciuto: {command}")
            return None

        reply_format = command_details.get("reply_format")
        placeholders = command_details.get("placeholder", [])
        if not reply_format or not placeholders:
            logging.error(f"\n\tFormato di risposta o placeholder mancanti per il comando: {command}")
            return None

        return command_details

    def parse_response(self, reply, command_details):
        """
        Esegue il parsing della risposta dalla telecamera.
        """
        reply_format = command_details.get("reply_format")
        placeholders = command_details.get("placeholder", [])

        # Rimuovi spazi nella risposta
        if isinstance(reply, tuple):
            raw_values = "".join(reply).replace(" ", "")
        else:
            raw_values = reply.replace(" ", "")

        expected_format = reply_format.replace(" ", "")

        results = {}
        index = 0

        for token in placeholders:
            if token == "pp":
                value = raw_values[index:index + 2]
                results[token] = int(value, 16)
                index += 2
            elif token == "p":
                value = raw_values[index]
                results[token] = int(value, 16)
                index += 1
            else:
                raise ValueError(f"Formato della risposta non valido: {reply_format}")

            logging.debug(f"\n\tToken: {token} - Value: {value} - Int Value: {results[token]}")

            # Correzione: Forza il mapping al valore Enum, se applicabile
            state_key = command_details.get("state")
            if state_key:
                enum_class = getattr(self.baseClass.state, state_key, None).__class__
                if enum_class and issubclass(enum_class, Enum):
                    for enum_item in enum_class:
                        if enum_item.value == results.get("pp"):
                            results[token] = enum_item  # Mappa direttamente all'enum
                            break

            return results

    def _combine_values(self, parsed_values, placeholders):
        """
        Combina i valori del parsing se necessario.
        """
        if len(parsed_values) == 1:
            return next(iter(parsed_values.values()))
        elif len(parsed_values) > 1:
            return tuple(parsed_values.values())
        else:
            raise ValueError(f"Errore durante la combinazione dei valori: {placeholders}")

    def _update_state(self, command, combined_value):
        """
        Aggiorna la variabile di stato corrispondente al comando.
        """
        state_key = self.command_map[command].get("state")
        if state_key:
            try:
                self.baseClass.state.set_state(state_key, combined_value)
                logging.info(f"\n\t{state_key} aggiornato a: {combined_value}")
            except AttributeError as e:
                logging.error(f"\n\tErrore durante l'aggiornamento dello stato: {e}")
        else:
            logging.error(f"\n\tComando '{command}' non ha una chiave di stato associata.")


