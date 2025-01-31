class MessagePacker:
    _cameraID = b'\x81'

    def __init__(self):
        self.sequence_number = 1

    @property
    def cameraID(self):
        return self._cameraID

    @cameraID.setter
    def cameraID(self, value):
        if not isinstance(value, bytes) or len(value) != 1:
            raise ValueError("cameraID deve essere un byte singolo.")
        self._cameraID = value

    def sequenceReset(self):
        self.sequence_number = 1

    def calculate_length(self, payload: bytes) -> bytes:
        """
        Calcola la lunghezza del payload in byte e la restituisce come due byte.
        :param payload: Comando payload in formato bytes.
        :return: Lunghezza del payload come 2 byte.
        """
        return len(payload).to_bytes(2, 'big')

    def build_command(self, payload: str) -> bytes:
        """
        Costruisce il comando completo aggiungendo header, sequenza e terminatore.
        :param payload: Comando payload come stringa esadecimale (es. "01 04 39 03").
        :return: Comando completo VISCA in formato bytes.
        """
        payload_type = b'\x01\x00'  # Identifica il tipo di messaggio
        terminator = b'\xff'
        payload_bytes = self.cameraID + bytes.fromhex(payload) + terminator
        # Lunghezza del payload
        payload_length = self.calculate_length(payload_bytes)
        # Numero di sequenza (4 byte)
        sequence_bytes = self.sequence_number.to_bytes(4, 'big')
        # Costruzione del messaggio
        message = payload_type + payload_length + sequence_bytes + payload_bytes

        # Incrementa la sequenza (ciclo tra 1 e 2^32-1)
        self.sequence_number = (self.sequence_number + 1) & 0xFFFFFFFF
        return message


if __name__ == "__main__":
    from visca.cameraObject import CameraObject
    from visca.dictionary.enumerations import ExposureModeEnum

    camera = CameraObject()
    packer = MessagePacker()

    command = camera.exposure.setExposureMode(ExposureModeEnum.MANUAL)
    print(command)
    packed_command = packer.build_command(command)
    print("Comando Binario (MANUAL):", packed_command)

    command = camera.exposure.setExposureMode(ExposureModeEnum.FULL_AUTO)
    packed_command = packer.build_command(command)
    print("Comando Binario (FULL_AUTO):", packed_command)

    command = camera.exposure.getExposureMode()
    packed_command = packer.build_command(command)
    print("Comando Binario (GET):", packed_command)