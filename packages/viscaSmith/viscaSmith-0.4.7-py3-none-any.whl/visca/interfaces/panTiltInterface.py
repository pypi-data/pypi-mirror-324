from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.panTiltMemories import PanTiltMemories

class PanTiltInterface(BaseInterfaceClass):
    def __init__(self, _panTiltMemories: PanTiltMemories, _panTiltDictionary: dict):
        super().__init__()
        self.panTiltMemories = _panTiltMemories
        self.command_map = _panTiltDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # Validazione delle velocità
    @staticmethod
    def _validate_speed(pan_speed: int, tilt_speed: int):
        if not (1 <= pan_speed <= 18):
            raise ValueError("Pan speed deve essere compresa tra 1 e 18.")
        if not (1 <= tilt_speed <= 17):
            raise ValueError("Tilt speed deve essere compresa tra 1 e 17.")

    # Pan-Tilt Drive Up
    def panTiltDriveUp(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveUp", pan_speed, tilt_speed)

    # Pan-Tilt Drive Down
    def panTiltDriveDown(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveDown", pan_speed, tilt_speed)

    # Pan-Tilt Drive Left
    def panTiltDriveLeft(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveLeft", pan_speed, tilt_speed)

    # Pan-Tilt Drive Right
    def panTiltDriveRight(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveRight", pan_speed, tilt_speed)

    # Pan-Tilt Drive Up-Left
    def panTiltDriveUpLeft(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveUpLeft", pan_speed, tilt_speed)

    # Pan-Tilt Drive Up-Right
    def panTiltDriveUpRight(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveUpRight", pan_speed, tilt_speed)

    # Pan-Tilt Drive Down-Left
    def panTiltDriveDownLeft(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveDownLeft", pan_speed, tilt_speed)

    # Pan-Tilt Drive Down-Right
    def panTiltDriveDownRight(self, pan_speed: int, tilt_speed: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._last_command = None
        return self.processor.set("panTiltDriveDownRight", pan_speed, tilt_speed)

    # Pan-Tilt Drive Stop
    def panTiltDriveStop(self):
        self._last_command = None
        return self.processor.set("panTiltDriveStop", self.panTiltMemories.panSpeed, self.panTiltMemories.tiltSpeed)

    # Pan-Tilt Absolute Position
    def panTiltAbsolutePosition(self, pan_speed: int, tilt_speed: int, pan_position: int, tilt_position: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._validate_position(pan_position, tilt_position)
        self.panTiltMemories.pan_position = pan_position
        self.panTiltMemories.tilt_position = tilt_position
        self._last_command = None
        return self.processor.set("panTiltAbsolutePosition", pan_speed, tilt_speed, pan_position, tilt_position)

    # Pan-Tilt Relative Position
    def panTiltRelativePosition(self, pan_speed: int, tilt_speed: int, pan_position: int, tilt_position: int):
        self._validate_speed(pan_speed, tilt_speed)
        self._validate_position(pan_position, tilt_position)
        self.panTiltMemories.pan_position = pan_position
        self.panTiltMemories.tilt_position = tilt_position
        self._last_command = None
        return self.processor.set("panTiltRelativePosition", pan_speed, tilt_speed, pan_position, tilt_position)

    # Pan-Tilt Home
    def panTiltHome(self):
        self._last_command = None
        return self.processor.set("panTiltHome")

    # Pan-Tilt Reset
    def panTiltReset(self):
        self._last_command = None
        return self.processor.set("panTiltReset")

    # Pan-Tilt Ramp Curve
    def panTiltRampCurve(self, value: int):
        self._last_command = None
        return self.processor.set("panTiltRampCurve", value)

    # Pan-Tilt Slow
    def panTiltSlow(self, mode: EnableStateEnum):
        self._last_command = None
        self.panTiltMemories.pan_tilt_slowMode = mode
        return self.processor.set("panTiltSlow", mode.value)

    # Pan-Tilt Limit Set
    def panTiltLimitSet(self, position: int, pan_position: int, tilt_position: int):
        self._validate_position(pan_position, tilt_position)
        self._last_command = None
        return self.processor.set("panTiltLimitSet", position, pan_position, tilt_position)

    # Pan-Tilt Limit Clear
    def panTiltLimitClear(self, position: int):
        self._last_command = None
        return self.processor.set("panTiltLimitClear", position)

    @staticmethod
    def _validate_position(pan_position: int, tilt_position: int):
        if not (0x0000 <= pan_position <= 0xFFFF):
            raise ValueError("Posizione Pan fuori range (0000-FFFF).")
        if not (0x0000 <= tilt_position <= 0xFFFF):
            raise ValueError("Posizione Tilt fuori range (0000-FFFF).")

if __name__ == "__main__":
    panTiltMemories = PanTiltMemories()
    panTiltDictionary = VISCADICTIONARY["PanTiltSettings"]
    interface = PanTiltInterface(panTiltMemories, panTiltDictionary)

    # Pan-Tilt Drive Up
    print("Pan-Tilt Drive Up:", interface.panTiltDriveUp(10, 8))

    # Pan-Tilt Drive Down
    print("Pan-Tilt Drive Down:", interface.panTiltDriveDown(10, 8))

    # Pan-Tilt Drive Left
    print("Pan-Tilt Drive Left:", interface.panTiltDriveLeft(10, 8))

    # Pan-Tilt Drive Right
    print("Pan-Tilt Drive Right:", interface.panTiltDriveRight(10, 8))

    # Pan-Tilt Drive Stop
    print("Pan-Tilt Drive Stop:", interface.panTiltDriveStop())

    # Pan-Tilt Absolute Position
    print("Pan-Tilt Absolute Position:", interface.panTiltAbsolutePosition(10, 8, 0x1000, 0x0800))

    # Pan-Tilt Relative Position
    print("Pan-Tilt Relative Position:", interface.panTiltRelativePosition(10, 8, 0x0010, 0x0020))

    # Pan-Tilt Home
    print("Pan-Tilt Home:", interface.panTiltHome())

    # Pan-Tilt Reset
    print("Pan-Tilt Reset:", interface.panTiltReset())

    # Pan-Tilt Ramp Curve
    print("Pan-Tilt Ramp Curve:", interface.panTiltRampCurve(1))

    # Pan-Tilt Slow (Enable)
    print("Pan-Tilt Slow (Enable):", interface.panTiltSlow(EnableStateEnum.ON))

    # Pan-Tilt Slow (Disable)
    print("Pan-Tilt Slow (Disable):", interface.panTiltSlow(EnableStateEnum.OFF))

    # Pan-Tilt Limit Set
    #print("Pan-Tilt Limit Set:", interface.panTiltLimitSet(1, 0x1000, 0x0800))

    # Pan-Tilt Limit Clear
    print("Pan-Tilt Limit Clear:", interface.panTiltLimitClear(0))

    # Test invalid values
    try:
        print("Invalid Speed (Pan):", interface.panTiltDriveUp(20, 8))  # Velocità Pan fuori range
    except ValueError as e:
        print("Errore:", e)

    try:
        print("Invalid Speed (Tilt):", interface.panTiltDriveDown(10, 20))  # Velocità Tilt fuori range
    except ValueError as e:
        print("Errore:", e)

    try:
        print("Invalid Position (Pan):",
              interface.panTiltAbsolutePosition(10, 8, 0x10000, 0x0800))  # Posizione Pan fuori range
    except ValueError as e:
        print("Errore:", e)

    try:
        print("Invalid Position (Tilt):",
              interface.panTiltRelativePosition(10, 8, 0x1000, 0x10000))  # Posizione Tilt fuori range
    except ValueError as e:
        print("Errore:", e)

    try:
        print("Invalid Ramp Curve:", interface.panTiltRampCurve(2))  # Valore non valido per Ramp Curve
    except ValueError as e:
        print("Errore:", e)


    try:
        print("Invalid Pan-Tilt Limit Set:", interface.panTiltLimitSet(2, 0x1000, 0x0800))  # Posizione non valida
    except ValueError as e:
        print("Errore:", e)

