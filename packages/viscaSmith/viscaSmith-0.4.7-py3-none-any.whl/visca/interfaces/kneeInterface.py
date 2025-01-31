from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.kneeMemories import KneeMemories


class KneeInterface(BaseInterfaceClass):

    def __init__(self, _kneeMemories: KneeMemories, _kneeDictionary: dict):
        super().__init__()
        self.kneeMemories = _kneeMemories
        self.command_map = _kneeDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setKneeSetting(self, mode: EnableStateEnum):
        """
        Abilita o disabilita il Knee Setting.

        Valori disponibili:
        - **2**: Disabilitato.
        - **3**: Abilitato.

        :param mode: Stato del Knee Setting ON/OFF.
        :return: Comando inviato.
        """

        self._last_command = None
        self.kneeMemories.knee_setting = mode
        return self.processor.set("kneeSetting", mode.value)

    def getKneeSetting(self):
        self._last_command = "get kneeSetting"
        return self.processor.inquire("kneeSetting")

    # Knee Mode
    def setKneeMode(self, mode: KneeEnum):
        """
        Imposta la modalità Knee.

        Valori disponibili:
        - **0**: Modalità Auto.
        - **4**: Modalità Manual.

        :param mode:
        :param value: Modalità Knee.
        :return: Comando inviato.
        """

        self._last_command = None
        self.kneeMemories.knee_mode = mode
        return self.processor.set("kneeMode", mode.value)

    def getKneeMode(self):
        self._last_command = "get kneeMode"
        return self.processor.inquire("kneeMode")

    # Knee Slope Value
    def setKneeSlopeValue(self, value: int):
        """
        Imposta la pendenza (slope) del Knee.

        Valori disponibili:
        -7 a +7
        - **0-14**: Valori da 0x00 a 0x0E.

        :param value: Valore della pendenza.
        :return: Comando inviato.
        """
        if value < -7 or value > 7:
            raise ValueError("Valore fuori range per Knee Slope Value (-7, 7).")
        self._last_command = None
        self.kneeMemories.knee_slope_value = value
        value = value + 7
        return self.processor.set("kneeSlopeValue", value)

    def getKneeSlopeValue(self):
        self._last_command = "get kneeSlopeValue"
        return self.processor.inquire("kneeSlopeValue")

    # Knee Point Value
    def setKneePointValue(self, value: int):
        """
        Imposta il punto Knee.

        Valori disponibili:
        - **0-12**: Valori da 0x00 a 0x0C.

        :param value: Valore del punto Knee.
        :return: Comando inviato.
        """
        if value < 0 or value > 12:
            raise ValueError("Valore fuori range per Knee Point Value (0, 12).")
        self._last_command = None
        self.kneeMemories.knee_point_value = value
        return self.processor.set("kneePointValue", value)

    def getKneePointValue(self):
        self._last_command = "get kneePointValue"
        return self.processor.inquire("kneePointValue")

if __name__ == "__main__":
    kneeMemories = KneeMemories()
    kneeDictionary = VISCADICTIONARY["KneeSettings"]
    kneeInterface = KneeInterface(kneeMemories, kneeDictionary)

    print("\nTESTING setKneeSetting")
    print(kneeInterface.setKneeSetting(EnableStateEnum.OFF))
    print(kneeInterface.setKneeSetting(EnableStateEnum.ON))

    print("\nTESTING getKneeSetting")
    print(kneeInterface.getKneeSetting())

    print("\nTESTING setKneeMode")
    print(kneeInterface.setKneeMode(KneeEnum.AUTO))
    print(kneeInterface.setKneeMode(KneeEnum.MANUAL))

    print("\nTESTING getKneeMode")
    print(kneeInterface.getKneeMode())

    print("\nTESTING setKneeSlopeValue")
    print(kneeInterface.setKneeSlopeValue(0))
    print(kneeInterface.setKneeSlopeValue(-7))
    print(kneeInterface.setKneeSlopeValue(7))

    print("\nTESTING getKneeSlopeValue")
    print(kneeInterface.getKneeSlopeValue())

    print("\nTESTING setKneePointValue")
    print(kneeInterface.setKneePointValue(0))
    print(kneeInterface.setKneePointValue(12))
    print(kneeInterface.setKneePointValue(6))

    print("\nTESTING getKneePointValue")
    print(kneeInterface.getKneePointValue())