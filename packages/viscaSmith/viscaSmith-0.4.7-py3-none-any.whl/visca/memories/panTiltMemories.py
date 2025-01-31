from visca.dictionary.enumerations import *


class PanTiltMemories:
    """
    Classe per gestire i valori di memoria del Pan/Tilt di una telecamera VISCA.
    """

    def __init__(self):
        self._pan_speed = 1
        self._tilt_speed = 1
        self._pan_position = 0
        self._tilt_position = 0
        self._pan_tilt_slow_mode = EnableStateEnum.OFF

    @property
    def panSpeed(self):
        return self._pan_speed

    @panSpeed.setter
    def panSpeed(self, speed: int):
        self._pan_speed = speed

    @property
    def tiltSpeed(self):
        return self._tilt_speed

    @tiltSpeed.setter
    def tiltSpeed(self, speed: int):
        self._tilt_speed = speed

    @property
    def panPosition(self):
        return self._pan_position

    @panPosition.setter
    def panPosition(self, position: int):
        self._pan_position = position

    @property
    def tiltPosition(self):
        return self._tilt_position

    @tiltPosition.setter
    def tiltPosition(self, position: int):
        self._tilt_position = position

    @property
    def panTiltSlowMode(self):
        return self._pan_tilt_slow_mode

    @panTiltSlowMode.setter
    def panTiltSlowMode(self, mode: EnableStateEnum):
        self._pan_tilt_slow_mode = mode

    def serialize(self):
        """
        Converte l'oggetto in un dizionario serializzabile.
        """
        return {
            "panSpeed": self._pan_speed,
            "tiltSpeed": self._tilt_speed,
            "panPosition": self._pan_position,
            "tiltPosition": self._tilt_position,
            "panTiltSlowMode": self._pan_tilt_slow_mode.name,  # Enum salvato come stringa
        }

    def deserialize(self, data):
        """
        Carica i valori da un dizionario.
        """
        self._pan_speed = data.get("panSpeed", self._pan_speed)
        self._tilt_speed = data.get("tiltSpeed", self._tilt_speed)
        self._pan_position = data.get("panPosition", self._pan_position)
        self._tilt_position = data.get("tiltPosition", self._tilt_position)
        self._pan_tilt_slow_mode = self.returnEnumerationFromSomething(
            data.get("panTiltSlowMode", self._pan_tilt_slow_mode.name), EnableStateEnum
        )

    @staticmethod
    def returnEnumerationFromSomething(value, enumeration):
        """
        Converte un valore in un'istanza dell'enumerazione specificata.
        """
        try:
            if isinstance(value, enumeration):
                return value  # È già un'istanza dell'enumerazione
            elif isinstance(value, int):
                return enumeration(value)  # Converte direttamente dall'intero
            elif isinstance(value, str):
                # Prova a convertire da nome Enum
                if value in enumeration.__members__:
                    return enumeration[value]
                return enumeration(int(value))  # Prova con intero
            else:
                raise ValueError(f"Impossibile convertire il valore '{value}' in {enumeration.__name__}.")
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"Errore durante la conversione di '{value}' in {enumeration.__name__}: {e}")
