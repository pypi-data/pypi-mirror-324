
from visca.dictionary.enumerations import *


class KneeMemories:
    # Valori di default
    _knee_setting: EnableStateEnum
    _knee_mode: KneeEnum
    _knee_slope_value: int
    _knee_point_value: int

    def __init__(self):
        self._knee_setting = EnableStateEnum.OFF
        self._knee_mode = KneeEnum.AUTO
        self._knee_slope_value = 0
        self._knee_point_value = 0

    @property
    def kneeSetting(self):
        return self._knee_setting

    @kneeSetting.setter
    def kneeSetting(self, mode: EnableStateEnum):
        self._knee_setting = mode

    @property
    def kneeMode(self):
        return self._knee_mode

    @kneeMode.setter
    def kneeMode(self, mode: KneeEnum):
        self._knee_mode = mode

    @property
    def kneeSlopeValue(self):
        return self._knee_slope_value

    @kneeSlopeValue.setter
    def kneeSlopeValue(self, value: int):
        self._knee_slope_value = value

    @property
    def kneePointValue(self):
        return self._knee_point_value

    @kneePointValue.setter
    def kneePointValue(self, value: int):
        self._knee_point_value = value

    def serialize(self):
        return {
            "kneeSetting": self._knee_setting.name,
            "kneeMode": self._knee_mode.name,
            "kneeSlopeValue": self._knee_slope_value,
            "kneePointValue": self._knee_point_value
        }

    def deserialize(self, data):
        """
        Carica i valori da un dizionario, gestendo eventuali valori mancanti.
        """
        self._knee_setting = self.returnEnumerationFromSomething(
            data.get("kneeSetting", self._knee_setting.name), EnableStateEnum
        )
        self._knee_mode = self.returnEnumerationFromSomething(
            data.get("kneeMode", self._knee_mode.name), KneeEnum
        )
        self._knee_slope_value = data.get("kneeSlopeValue", self._knee_slope_value)
        self._knee_point_value = data.get("kneePointValue", self._knee_point_value)

    @staticmethod
    def returnEnumerationFromSomething(something, enumeration):
        """
        Converte un valore in un'istanza dell'enumerazione specificata.

        :param something: Il valore da convertire.
        :param enumeration: L'enumerazione target.
        :return: Un'istanza dell'enumerazione.
        :raises ValueError: Se la conversione non è possibile.
        """
        try:
            if isinstance(something, enumeration):
                return something  # È già un'istanza dell'enumerazione
            elif isinstance(something, int):
                return enumeration(something)  # Converte direttamente dall'intero
            elif isinstance(something, str):
                # Prova prima a convertire dal nome dell'enumerazione
                if something in enumeration.__members__:
                    return enumeration[something]
                # Se non è un nome, prova a convertirlo in un intero
                num = int(something)
                return enumeration(num)
            else:
                raise ValueError(f"Impossibile convertire il valore '{something}' in {enumeration.__name__}.")
        except (ValueError, KeyError, TypeError) as e:
            raise ValueError(f"Errore durante la conversione di '{something}' in {enumeration.__name__}: {e}")
