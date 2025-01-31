from visca.dictionary.enumerations import *


class SystemMemories:
    """
    Classe per gestire i parametri di sistema della telecamera VISCA.
    """

    def __init__(self):
        # Variabili di stato
        self._ir_receive = EnableStateEnum.OFF
        self._h_phase_value = 0  # Default iniziale
        self._img_flip = EnableStateEnum.OFF
        self._camera_id = 0
        self._menu_mode = EnableStateEnum.OFF
        self._ir_cut_filter = EnableStateEnum.OFF
        self._tally_mode = EnableStateEnum.ON
        self._tally_level = TallyLevel.HIGH
        self._hdmi_color_space = HdmiColorFormatEnum.YCbCr
        self._power_state = 2

    @property
    def irReceive(self):
        return self._ir_receive

    @irReceive.setter
    def irReceive(self, value: EnableStateEnum):
        self._ir_receive = value

    @property
    def hPhaseValue(self):
        return self._h_phase_value

    @hPhaseValue.setter
    def hPhaseValue(self, value: int):
        self._h_phase_value = value

    @property
    def imgFlip(self):
        return self._img_flip

    @imgFlip.setter
    def imgFlip(self, value: EnableStateEnum):
        self._img_flip = value

    @property
    def cameraId(self):
        return self._camera_id

    @cameraId.setter
    def cameraId(self, value: int):
        self._camera_id = value

    @property
    def menuMode(self):
        return self._menu_mode

    @menuMode.setter
    def menuMode(self, value: EnableStateEnum):
        self._menu_mode = value

    @property
    def irCutFilter(self):
        return self._ir_cut_filter

    @irCutFilter.setter
    def irCutFilter(self, value: EnableStateEnum):
        self._ir_cut_filter = value

    @property
    def tallyMode(self):
        return self._tally_mode

    @tallyMode.setter
    def tallyMode(self, value: EnableStateEnum):
        self._tally_mode = value

    @property
    def tallyLevel(self):
        return self._tally_level

    @tallyLevel.setter
    def tallyLevel(self, value: TallyLevel):
        self._tally_level = value

    @property
    def hdmiColorSpace(self):
        return self._hdmi_color_space

    @hdmiColorSpace.setter
    def hdmiColorSpace(self, value: HdmiColorFormatEnum):
        self._hdmi_color_space = value

    @property
    def powerState(self):
        return self._power_state

    @powerState.setter
    def powerState(self, value: int):
        self._power_state = value

    def serialize(self):
        """
        Converte l'oggetto in un dizionario serializzabile (compatibile con JSON).
        """
        return {
            "irReceive": self._ir_receive.name,
            "hPhaseValue": self._h_phase_value,
            "imgFlip": self._img_flip.name,
            "cameraId": self._camera_id,
            "menuMode": self._menu_mode.name,
            "irCutFilter": self._ir_cut_filter.name,
            "tallyMode": self._tally_mode.name,
            "tallyLevel": self._tally_level.name,
            "hdmiColorSpace": self._hdmi_color_space.name,
            "powerState": self._power_state
        }

    def deserialize(self, data: dict):
        """
        Carica i valori da un dizionario, convertendo le stringhe negli Enum corretti.
        """
        self._ir_receive = self.returnEnumerationFromSomething(data.get("irReceive", self._ir_receive.name), EnableStateEnum)
        self._h_phase_value = data.get("hPhaseValue", self._h_phase_value)
        self._img_flip = self.returnEnumerationFromSomething(data.get("imgFlip", self._img_flip.name), EnableStateEnum)
        self._camera_id = data.get("cameraId", self._camera_id)
        self._menu_mode = self.returnEnumerationFromSomething(data.get("menuMode", self._menu_mode.name), EnableStateEnum)
        self._ir_cut_filter = self.returnEnumerationFromSomething(data.get("irCutFilter", self._ir_cut_filter.name), EnableStateEnum)
        self._tally_mode = self.returnEnumerationFromSomething(data.get("tallyMode", self._tally_mode.name), EnableStateEnum)
        self._tally_level = self.returnEnumerationFromSomething(data.get("tallyLevel", self._tally_level.name), TallyLevel)
        self._hdmi_color_space = self.returnEnumerationFromSomething(data.get("hdmiColorSpace", self._hdmi_color_space.name), HdmiColorFormatEnum)
        self._power_state = data.get("powerState", self._power_state)

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
