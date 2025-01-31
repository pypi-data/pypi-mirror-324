from visca.dictionary.enumerations import *


class GammaMemories:

    _gamma_select: GammaLevelEnum
    _gamma_pattern_value: int
    _gamma_offset_value: dict
    _gamma_level_value: int
    _black_gamma_level_value: int
    _black_gamma_range_value: BlackGammaRangeEnum
    _black_level_value: int

    def __init__(self):
        # Stato iniziale
        self._gamma_select = GammaLevelEnum.STD
        self._gamma_pattern_value = 0
        self._gamma_offset_value = {"polarity": GammaPolarityEnum.POSITIVE, "width": 0}
        self._gamma_level_value = 0
        self._black_gamma_level_value = 0
        self._black_gamma_range_value = BlackGammaRangeEnum.MIDDLE
        self._black_level_value = 0

    @property
    def gammaSelect(self):
        return self._gamma_select

    @gammaSelect.setter
    def gammaSelect(self, value):
        self._gamma_select = value

    @property
    def gammaPatternValue(self):
        return self._gamma_pattern_value

    @gammaPatternValue.setter
    def gammaPatternValue(self, value):
        self._gamma_pattern_value = value

    @property
    def gammaOffsetValue(self):
        return self._gamma_offset_value

    @gammaOffsetValue.setter
    def gammaOffsetValue(self, value: dict):
        self._gamma_offset_value = value

    @property
    def gammaLevelValue(self):
        return self._gamma_level_value

    @gammaLevelValue.setter
    def gammaLevelValue(self, value):
        self._gamma_level_value = value

    @property
    def blackGammaLevelValue(self):
        return self._black_gamma_level_value

    @blackGammaLevelValue.setter
    def blackGammaLevelValue(self, value):
        self._black_gamma_level_value = value

    @property
    def blackGammaRangeValue(self):
        return self._black_gamma_range_value

    @blackGammaRangeValue.setter
    def blackGammaRangeValue(self, value: BlackGammaRangeEnum):
        self._black_gamma_range_value = value

    @property
    def blackLevelValue(self):
        return self._black_level_value

    @blackLevelValue.setter
    def blackLevelValue(self, value):
        self._black_level_value = value

    def serialize(self):
        return {
            "gammaSelect": self._gamma_select.name,
            "gammaPatternValue": self._gamma_pattern_value,
            "gammaOffsetValue": self._gamma_offset_value,
            "gammaLevelValue": self._gamma_level_value,
            "blackGammaLevelValue": self._black_gamma_level_value,
            "blackGammaRangeValue": self._black_gamma_range_value.name,
            "blackLevelValue": self._black_level_value,
        }

    def deserialize(self, data):
        self.gammaSelect = self.returnEnumerationFromSomething(data.get("gammaSelect"), GammaLevelEnum)
        self.gammaPatternValue = data.get("gammaPatternValue", self.gammaPatternValue)
        self.gammaOffsetValue = data.get("gammaOffsetValue", self.gammaOffsetValue)
        self.gammaLevelValue = data.get("gammaLevelValue", self.gammaLevelValue)
        self.blackGammaLevelValue = data.get("blackGammaLevelValue", self.blackGammaLevelValue)
        self.blackGammaRangeValue = self.returnEnumerationFromSomething(data.get("blackGammaRangeValue"), BlackGammaRangeEnum)
        self.blackLevelValue = data.get("blackLevelValue", self.blackLevelValue)

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
