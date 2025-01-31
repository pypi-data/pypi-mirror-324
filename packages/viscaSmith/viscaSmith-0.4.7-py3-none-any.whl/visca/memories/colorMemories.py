from visca.dictionary.enumerations import *


class ColorMemories:

    _whiteBalanceMode: WhiteBalanceModeEnum
    _wbSpeed: int
    _offset: int
    _rGain: int
    _bGain: int
    _matrix: MatrixSelectEnum
    _saturation: int
    _chromaSuppression: ChromaSuppressionEnum
    _phase: int
    _rG: int
    _rB: int
    _gR: int
    _gB: int
    _bR: int
    _bG: int

    def __init__(self):
        self._whiteBalanceMode = WhiteBalanceModeEnum.MANUAL
        self._wbSpeed = 1
        self._offset = 0
        self._rGain = 0
        self._bGain = 0
        self._matrix = MatrixSelectEnum.OFF
        self._saturation = 4
        self._chromaSuppression = ChromaSuppressionEnum.OFF
        self._phase = 0
        self._rG = 0
        self._rB = 0
        self._gR = 0
        self._gB = 0
        self._bR = 0
        self._bG = 0

    @property
    def whiteBalanceMode(self):
        return self._whiteBalanceMode

    @whiteBalanceMode.setter
    def whiteBalanceMode(self, value):
        self._whiteBalanceMode = value

    @property
    def wbSpeed(self):
        return self._wbSpeed

    @wbSpeed.setter
    def wbSpeed(self, value):
        self._wbSpeed = value

    @property
    def offsetValue(self):
        return self._offset

    @offsetValue.setter
    def offsetValue(self, value):
        self._offset = value

    @property
    def rGain(self):
        return self._rGain

    @rGain.setter
    def rGain(self, value):
        self._rGain = value

    @property
    def bGain(self):
        return self._bGain

    @bGain.setter
    def bGain(self, value):
        self._bGain = value

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value

    @property
    def saturation(self):
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = value

    @property
    def chromaSuppression(self):
        return self._chromaSuppression

    @chromaSuppression.setter
    def chromaSuppression(self, value: ChromaSuppressionEnum):
        self._chromaSuppression = value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value

    @property
    def rG(self):
        return self._rG

    @rG.setter
    def rG(self, value):
        self._rG = value

    @property
    def rB(self):
        return self._rB

    @rB.setter
    def rB(self, value):
        self._rB = value

    @property
    def gR(self):
        return self._gR

    @gR.setter
    def gR(self, value):
        self._gR = value

    @property
    def gB(self):
        return self._gB

    @gB.setter
    def gB(self, value):
        self._gB = value

    @property
    def bR(self):
        return self._bR

    @bR.setter
    def bR(self, value):
        self._bR = value

    @property
    def bG(self):
        return self._bG

    @bG.setter
    def bG(self, value):
        self._bG = value


    def serialize(self):
        return {
            "whiteBalanceMode": self._whiteBalanceMode,
            "wbSpeed": self._wbSpeed,
            "offset": self._offset,
            "rGain": self._rGain,
            "bGain": self._bGain,
            "matrix": self._matrix,
            "saturation": self._saturation,
            "chromaSuppression": self._chromaSuppression,
            "phase": self._phase,
            "rG": self._rG,
            "rB": self._rB,
            "gR": self._gR,
            "gB": self._gB,
            "bR": self._bR,
            "bG": self._bG,
        }

    def deserialize(self, data):
        self._whiteBalanceMode = self.returnEnumerationFromSomething(
            data.get("whiteBalanceMode", self._whiteBalanceMode), WhiteBalanceModeEnum)
        self._wbSpeed = data.get("wbSpeed", self._wbSpeed)
        self._offset = data.get("offset", self._offset)
        self._rGain = data.get("rGain", self._rGain)
        self._bGain = data.get("bGain", self._bGain)

        self._matrix = self.returnEnumerationFromSomething(data['matrix'], MatrixSelectEnum)
        self._saturation = data.get("saturation", self._saturation)
        self._chromaSuppression = self.returnEnumerationFromSomething(
            data.get("chromaSuppression", self._chromaSuppression), ChromaSuppressionEnum)
        self._phase = data.get("phase", self._phase)
        self._rG = data.get("rG", self._rG)
        self._rB = data.get("rB", self._rB)
        self._gR = data.get("gR", self._gR)
        self._gB = data.get("gB", self._gB)
        self._bR = data.get("bR", self._bR)
        self._bG = data.get("bG", self._bG)


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
