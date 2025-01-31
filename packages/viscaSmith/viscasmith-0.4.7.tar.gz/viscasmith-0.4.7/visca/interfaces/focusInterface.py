from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.focusMemories import FocusMemories



class FocusDistanceMapper:
    focus_map = {
        0x1000: float('inf'),  # Infinity
        0x2000: 5.0,          # 5 meters
        0x3000: 3.0,          # 3 meters
        0x4000: 2.0,          # 2 meters
        0x5000: 1.5,          # 1.5 meters
        0x6000: 1.2,          # 1.2 meters
        0x7000: 1.0,          # 1 meter
        0x8000: 0.8,          # 0.8 meters
        0x9000: 0.6,          # 0.6 meters
        0xA000: 0.47,         # 0.47 meters
        0xB000: 0.35,         # 0.35 meters
        0xC000: 0.26,         # 0.26 meters
        0xD000: 0.17,         # 0.17 meters
        0xE000: 0.1,          # 0.1 meters
        0xF000: 0.08          # 0.08 meters
    }

    @staticmethod
    def get_focus_distance(focus_value: int) -> float:
        """
        Restituisce la distanza di messa a fuoco corrispondente al valore esadecimale.
        :param focus_value: Valore di messa a fuoco (esadecimale).
        :return: Distanza in metri.
        """
        return FocusDistanceMapper.focus_map.get(focus_value, None)


class FocusInterface(BaseInterfaceClass):

    def __init__(self, _focusMemories, _focusDictionary):
        super().__init__()
        self.focusMemories = _focusMemories
        self.command_map = _focusDictionary  # Assegna il dizionario dei comandi
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # Focus Mode
    def setFocusMode(self, mode: FocusModeEnum):
        """
        Imposta la modalità di messa a fuoco (Auto, Manuale o Toggle).
        :param mode: FocusModeEnum
        """
        self._last_command = None
        self.focusMemories.focus_mode = mode
        return self.processor.set("focusMode", mode.value)

    def getFocusMode(self):
        self._last_command = "get focusMode"
        return self.processor.inquire("focusMode")

    # Focus Movement
    def focusStop(self):
        """Ferma la messa a fuoco."""
        self._last_command = None
        return self.processor.set("focusStop")

    def focusFarStandard(self):
        """Muove la messa a fuoco verso lontano (velocità standard)."""
        self._last_command = None
        return self.processor.set("focusFarStandard")

    def focusNearStandard(self):
        """Muove la messa a fuoco verso vicino (velocità standard)."""
        self._last_command = None
        return self.processor.set("focusNearStandard")

    def setFocusFarVariable(self, speed: int):
        """
        Muove la messa a fuoco verso lontano con velocità variabile.
        :param speed: Velocità da 0 a 7.
        """
        if 0 > speed or speed > 7:
            raise ValueError("Valore fuori range per la velocità variabile.")
        self._last_command = None
        return self.processor.set("focusFarVariable", speed)

    def setFocusNearVariable(self, speed: int):
        """
        Muove la messa a fuoco verso vicino con velocità variabile.
        :param speed: Velocità da 0 a 7.
        """
        if 0 > speed or speed > 7:
            raise ValueError("Valore fuori range per la velocità variabile.")
        self._last_command = None
        return self.processor.set("focusNearVariable", speed)

    def setFocusValue(self, focus_value: int):
        """
        Imposta direttamente la posizione della messa a fuoco.
        :param focus_value: Valore intero esadecimale (0x0000 a 0xFFFF).
        """
        if focus_value < 0x0000 or focus_value > 0xFFFF:
            raise ValueError("Valore fuori range per la posizione della messa a fuoco.")

        self._last_command = None
        self.focusMemories.focus_value = focus_value

        # Passa i due byte separatamente
        return self.processor.set("focusValue", focus_value)

    def getFocusValue(self):
        self._last_command = "get focusValue"
        return self.processor.inquire("focusValue")

    # Additional Commands
    def focusOnePushTrigger(self):
        """Attiva il trigger AF One Push."""
        self._last_command = None
        return self.processor.set("focusOnePushTrigger")

    def focusInfinity(self):
        """Imposta la messa a fuoco all'infinito."""
        self._last_command = None
        return self.processor.set("focusInfinity")

    def setNearFocusLimit(self, focus_limit: int):
        """
        Imposta il limite di messa a fuoco più vicino.
        :param focus_limit: Valore esadecimale (0x0000 a 0xFFFF).
        """
        if focus_limit < 0x0000 or focus_limit > 0xFFFF:
            raise ValueError("Valore fuori range per il limite di messa a fuoco.")

        self._last_command = None
        self.focusMemories.focus_near_limit = focus_limit
        return self.processor.set("focusNearLimit", focus_limit)

    def setAfMode(self, mode: AutoFocusModeEnum):
        """
        Imposta la modalità Auto Focus (AF).
        :param mode: AutoFocusModeEnum
        """
        self._last_command = None
        self.focusMemories.af_mode = mode
        return self.processor.set("afMode", mode.value)

    def getAfMode(self):
        self._last_command = "get afMode"
        return self.processor.inquire("afMode")

    def setAfSensitivity(self, sensitivity: AutoFocusSensitivityEnum):
        """
        Imposta la sensibilità dell'AF.
        :param sensitivity: AutoFocusSensitivityEnum
        """
        self._last_command = None
        self.focusMemories.af_sensitivity = sensitivity
        return self.processor.set("afSensitivity", sensitivity.value)

    def setAfModeInterval(self, af_operatingTime: AutoFocusOperationTime, af_stay_time: int):
        """
        Imposta una modalità AF Speciale dove AutofocusMode è impostato su "NORMAL" di default, ma può essere
        modificato per un tempo specifico o azionato dallo zoom.
        af_stay_Time invece è un numero da 0 a 255 che rappresenta il tempo di attesa in secondi.
        0 = Disabilitato. 1-255 = Tempo di attesa in secondi.
        :param af_operatingTime: AutoFocusOperationTime NORMAL, INTERVAL, ZOOM
        :param af_stay_time: Tempo di attesa in secondi (0 a 255).
        """
        self._last_command = None
        self.focusMemories.af_operating_time = af_operatingTime
        self.focusMemories.af_stay_time = af_stay_time
        return self.processor.set("afModeInterval", af_operatingTime.value, af_stay_time)

    def getAfModeInterval(self):
        self._last_command = "get afModeInterval"
        return self.processor.inquire("afModeInterval")

    def getAfSensitivity(self):
        self._last_command = "get afSensitivity"
        return self.processor.inquire("afSensitivity")

    def setIrCorrection(self, correction: IRCorrectionEnum):
        """
        Imposta la correzione IR.
        :param correction: IRCorrectionEnum
        """
        self._last_command = None
        self.focusMemories.ir_correction = correction
        return self.processor.set("irCorrection", correction.value)

    def getIrCorrection(self):
        self._last_command = "get irCorrection"
        return self.processor.inquire("irCorrection")


if __name__ == "__main__":
    focusMemories = FocusMemories()
    focusDictionary = VISCADICTIONARY["FocusSettings"]
    focusInterface = FocusInterface(focusMemories, focusDictionary)

    print("=== Focus Interface Commands ===")

    print("Executing: setFocusMode(FocusModeEnum.AUTO)")
    print(focusInterface.setFocusMode(FocusModeEnum.AUTO))

    print("Executing: getFocusMode()")
    print(focusInterface.getFocusMode())

    print("Executing: focusStop()")
    print(focusInterface.focusStop())

    print("Executing: focusFarStandard()")
    print(focusInterface.focusFarStandard())

    print("Executing: focusNearStandard()")
    print(focusInterface.focusNearStandard())

    print("Executing: setFocusFarVariable(5)")
    print(focusInterface.setFocusFarVariable(5))

    print("Executing: setFocusNearVariable(5)")
    print(focusInterface.setFocusNearVariable(5))

    print("Executing: setFocusValue(123)")
    print(focusInterface.setFocusValue(123))

    print("Executing: getFocusValue()")
    print(focusInterface.getFocusValue())

    print("Executing: focusOnePushTrigger()")
    print(focusInterface.focusOnePushTrigger())

    print("Executing: focusInfinity()")
    print(focusInterface.focusInfinity())

    print("Executing: setNearFocusLimit(50)")
    print(focusInterface.setNearFocusLimit(50))

    print("Executing: setAfMode(AutoFocusModeEnum.NORMAL)")
    print(focusInterface.setAfMode(AutoFocusModeEnum.NORMAL))

    print("Executing: getAfMode()")
    print(focusInterface.getAfMode())

    print("Executing: setAfSensitivity(AutoFocusSensitivityEnum.NORMAL)")
    print(focusInterface.setAfSensitivity(AutoFocusSensitivityEnum.NORMAL))

    print("Executing: getAfSensitivity()")
    print(focusInterface.getAfSensitivity())

    print("Executing: setAfModeInterval(AutoFocusOperationTime.ZOOM_TRIGGER, 5)")
    print(focusInterface.setAfModeInterval(AutoFocusOperationTime.ZOOM_TRIGGER, 5))

    print("Executing: getAfModeInterval()")
    print(focusInterface.getAfModeInterval())

    print("Executing: setIrCorrection(IRCorrectionEnum.STANDARD)")
    print(focusInterface.setIrCorrection(IRCorrectionEnum.STANDARD))

    print("Executing: getIrCorrection()")
    print(focusInterface.getIrCorrection())

    print("Executing: focusStop()")
    print(focusInterface.focusStop())

    print("Executing: focusFarStandard()")
    print(focusInterface.focusFarStandard())

    print("Executing: focusNearStandard()")
    print(focusInterface.focusNearStandard())

    print("Executing: setFocusFarVariable(5)")
    print(focusInterface.setFocusFarVariable(5))

    print("Executing: setFocusNearVariable(5)")
    print(focusInterface.setFocusNearVariable(5))


