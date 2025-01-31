from visca.dictionary.enumerations import *


class FocusMemories:
    _focus_mode: FocusModeEnum
    _focus_value: int
    _af_mode: AutoFocusModeEnum
    _af_sensitivity: AutoFocusSensitivityEnum
    _ir_correction: IRCorrectionEnum

    def __init__(self):
        self._focus_mode = FocusModeEnum.AUTO
        self._focus_value = 0
        self._af_mode = AutoFocusModeEnum.NORMAL
        self._af_sensitivity = AutoFocusSensitivityEnum.NORMAL
        self._ir_correction = IRCorrectionEnum.STANDARD

    @property
    def focusMode(self):
        return self._focus_mode

    @focusMode.setter
    def focusMode(self, mode: FocusModeEnum):
        self._focus_mode = mode

    @property
    def focusValue(self):
        return self._focus_value

    @focusValue.setter
    def focusValue(self, value: int):
        self._focus_value = value

    @property
    def afMode(self):
        return self._af_mode

    @afMode.setter
    def afMode(self, mode: AutoFocusModeEnum):
        self._af_mode = mode

    @property
    def afSensitivity(self):
        return self._af_sensitivity

    @afSensitivity.setter
    def afSensitivity(self, sensitivity: AutoFocusSensitivityEnum):
        self._af_sensitivity = sensitivity

    @property
    def irCorrection(self):
        return self._ir_correction

    @irCorrection.setter
    def irCorrection(self, correction: IRCorrectionEnum):
        self._ir_correction = correction

    def serialize(self):
        return {
            "focus_mode": self._focus_mode.value,
            "focus_value": self._focus_value,
            "af_mode": self._af_mode.value,
            "af_sensitivity": self._af_sensitivity.value,
            "ir_correction": self._ir_correction.value
        }

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

    def deserialize(self, data):
        """
        Deserializza i dati e aggiorna gli attributi dell'oggetto.
        """
        self._focus_mode = self.returnEnumerationFromSomething(data.get("focus_mode"), FocusModeEnum)
        self._focus_value = data.get("focus_value")
        self._af_mode = self.returnEnumerationFromSomething(data.get("af_mode"), AutoFocusModeEnum)
        self._af_sensitivity = self.returnEnumerationFromSomething(data.get("af_sensitivity"), AutoFocusSensitivityEnum)
        self._ir_correction = self.returnEnumerationFromSomething(data.get("ir_correction"), IRCorrectionEnum)
