from visca.dictionary.enumerations import *


class ZoomMemories:
    """
    Classe per gestire i parametri di zoom della telecamera VISCA.
    """

    def __init__(self):
        # Stato iniziale
        self._zoom_mode = ZoomModeEnum.OPTICAL
        self._zoom_speed = 0
        self._zoom_value = 0
        self._tele_convert = EnableStateEnum.OFF

    @property
    def zoomMode(self):
        return self._zoom_mode

    @zoomMode.setter
    def zoomMode(self, mode: ZoomModeEnum):
        self._zoom_mode = mode

    @property
    def zoomSpeed(self):
        return self._zoom_speed

    @zoomSpeed.setter
    def zoomSpeed(self, speed: int):
        self._zoom_speed = speed

    @property
    def zoomValue(self):
        return self._zoom_value

    @zoomValue.setter
    def zoomValue(self, value: int):
        self._zoom_value = value

    @property
    def teleConvert(self):
        return self._tele_convert

    @teleConvert.setter
    def teleConvert(self, state: EnableStateEnum):
        self._tele_convert = state

    def serialize(self):
        """
        Converte l'oggetto in un dizionario serializzabile (compatibile con JSON).
        """
        return {
            "zoomMode": self._zoom_mode.name,
            "zoomSpeed": self._zoom_speed,
            "zoomValue": self._zoom_value,
            "teleConvert": self._tele_convert.name
        }

    def deserialize(self, data: dict):
        """
        Carica i valori da un dizionario, convertendo le stringhe negli Enum corretti.
        """
        self._zoom_mode = self.returnEnumerationFromSomething(data.get("zoomMode", self._zoom_mode.name), ZoomModeEnum)
        self._zoom_speed = data.get("zoomSpeed", self._zoom_speed)
        self._zoom_value = data.get("zoomValue", self._zoom_value)
        self._tele_convert = self.returnEnumerationFromSomething(data.get("teleConvert", self._tele_convert.name), EnableStateEnum)

    @staticmethod
    def returnEnumerationFromSomething(value, enumeration):
        """
        Converte un valore in un'istanza dell'enumerazione specificata.

        :param value: Il valore da convertire.
        :param enumeration: L'enumerazione target.
        :return: Un'istanza dell'enumerazione.
        :raises ValueError: Se la conversione non è possibile.
        """
        try:
            if isinstance(value, enumeration):
                return value  # È già un'istanza dell'enumerazione
            elif isinstance(value, int):
                return enumeration(value)  # Converte direttamente dall'intero
            elif isinstance(value, str):
                # Prova prima a convertire dal nome Enum
                if value in enumeration.__members__:
                    return enumeration[value]
                return enumeration(int(value))  # Prova con intero
            else:
                raise ValueError(f"Impossibile convertire il valore '{value}' in {enumeration.__name__}.")
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"Errore durante la conversione di '{value}' in {enumeration.__name__}: {e}")
