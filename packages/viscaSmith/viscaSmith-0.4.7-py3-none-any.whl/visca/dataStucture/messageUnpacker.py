class MessageUnpacker:
    """
    Classe helper per parsare i pacchetti VISCA over IP (formato base).

    Il formato tipico, semplificato, potrebbe essere:
    [byte0..1]   Tipo (es. 0x01 0x00)
    [byte2..3]   Lunghezza payload (2 byte, big-endian)
    [byte4..7]   Sequence number (4 byte, big-endian)
    [byte8..N]   Payload effettivo (cameraID + preambolo + contenuto)
                  ... eventuale terminator 0xFF ...
    """

    def __init__(self):
        pass  # se servono configurazioni iniziali, puoi aggiungerle

    @staticmethod
    def isAck(data: bytes) -> bool:
        """Verifica se il pacchetto è un ACK."""
        return data.startswith(b'\x02\xff')

    @staticmethod
    def isCompletion(data: bytes) -> bool:
        """Verifica se il pacchetto è un Completion."""
        return data.startswith(b'\x03\xff')

    @staticmethod
    def isError(data: bytes) -> bool:
        """Verifica se il pacchetto è un Error."""
        return data.startswith(b'\x04\xff')

    def unpack_message(self, data: bytes) -> dict:
        """
        Analizza il pacchetto ricevuto e restituisce un dizionario con:
        - message_type: Tipo del messaggio (es. "ack", "completion", "error", "command_set", ecc.)
        - sequence_number: Numero di sequenza (se presente)
        - payload: Contenuto grezzo del pacchetto (se presente)
        - camera_id: ID della camera (se presente)
        - preamble: Byte preambolo (se presente)
        - command_payload: Dati effettivi del comando (se presente)
        - raw_data: Il pacchetto originale
        """

        result = {
            "message_type": None,
            "sequence_number": None,
            "payload": b"",
            "camera_id": None,
            "preamble": None,
            "command_payload": b"",
            "raw_data": data,
            "error_code": None
        }

        if len(data) < 8:
            print(f" ❌ [unpack_message] Pacchetto troppo corto: {data.hex()}")
            result["message_type"] = "invalid"
            return result

        # Estrarre header e payload
        header = data[:8]
        seq_number = int.from_bytes(header[4:8], 'big')
        payload = data[8:]

        result["sequence_number"] = seq_number
        result["payload"] = payload

        print(f"Header: {header.hex()} | Payload: {payload.hex()} | Seq: {seq_number}")

        # Controllo messaggi speciali
        if self.isAck(payload):
            result["message_type"] = "ack"
            return result
        elif self.isCompletion(payload):
            result["message_type"] = "completion"
            return result
        elif self.isError(payload):
            print(f"\t ❌ ERROR FROM UNPACKER: {payload.hex()} | Message: {data.hex()}")
            result["message_type"] = "error"
            result["error_code"] = payload[1]
            print(f"\t ❌ Error code: {result['error_code']}")
            return result

        # Controllo se è una risposta a una richiesta "inquire"
        if payload.startswith(b'\x50'):
            return self.unpackInquireReply(payload, result)
        else:
            return self.unpackCommand(payload, result)


    def unpackInquireReply(self, payload: bytes, result: dict):
        print("Inquire reply detected")
        # Se termina con 0xFF, rimuovilo
        core = payload[1:-1] if payload.endswith(b'\xff') else payload[1:]

        # Se la risposta è a 1 o 2 byte, gestirla dinamicamente
        if len(core) == 1:
            value = int.from_bytes(core, "big", signed=True)  # Signed per supportare valori negativi
        elif len(core) == 2:
            value = int.from_bytes(core, "big", signed=True)
        else:
            value = core  # Se il formato non è chiaro, lascia il byte grezzo

        print(f"Core extracted: {core.hex()} | Decoded value: {value}")

        result.update({
            "message_type": "inquire_reply",
            "command_payload": core,
            "value": value  # Aggiungiamo anche il valore decodificato
        })
        return result

    def unpackCommand(self, payload: bytes, result: dict):
        # Interpretazione comando classico
        if len(payload) >= 2:
            result["camera_id"] = payload[0]
            result["preamble"] = payload[1]
            result["command_payload"] = payload[2:-1] if payload.endswith(b'\xff') else payload[2:]

            if result["preamble"] == 0x01:
                result["message_type"] = "command_set"
            elif result["preamble"] == 0x09:
                result["message_type"] = "command_inquire"
            else:
                result["message_type"] = "unknown_command"
        else:
            result["message_type"] = "invalid_payload"

        return result
