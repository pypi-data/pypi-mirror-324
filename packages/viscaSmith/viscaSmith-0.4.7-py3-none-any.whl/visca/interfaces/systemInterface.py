from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.systemMemories import SystemMemories


class SystemInterface(BaseInterfaceClass):

    def __init__(self, _systemMemories: SystemMemories, _systemDictionary: dict):
        super().__init__()
        self.systemMemories = _systemMemories
        self.command_map = _systemDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # IR Receive
    def setIRReceive(self, mode: EnableStateEnum):
        self.systemMemories.ir_receive = mode
        return self.processor.set("systemIrReceive", mode.value)

    # H Phase Up
    def hPhaseUp(self):
        if self.systemMemories.h_phase_value < 959:  # Max range 3BF (959 in decimale)
            self.systemMemories.h_phase_value += 1
        return self.processor.set("systemHPhaseUp")

    # H Phase Down
    def hPhaseDown(self):
        if self.systemMemories.h_phase_value > 0:
            self.systemMemories.h_phase_value -= 1
        return self.processor.set("systemHPhaseDown")

    # H Phase Value
    def setHPhaseValue(self, value: int):
        if value not in range(0, 960):  # Max range 3BF
            raise ValueError("Valore fuori range per H Phase Value.")
        self.systemMemories.h_phase_value = value
        return self.processor.set("systemHPhaseValue", value)

    # Image Flip
    def setImageFlip(self, mode: EnableStateEnum):
        self.systemMemories.img_flip = mode
        return self.processor.set("systemImgFlip", mode.value)

    # Camera ID
    def setCameraID(self, id_value: int):
        if id_value < int("0000", 16) or id_value > int("FFFF", 16):
            raise ValueError("ID Camera fuori range.")
        self.systemMemories.camera_id = id_value
        return self.processor.set("systemCameraId", id_value)

    # Menu Mode
    def setMenuMode(self, mode: EnableStateEnum):
        self.systemMemories.menu_mode = mode
        return self.processor.set("menuMode", mode.value)

    # Menu Enter
    def menuEnter(self):
        return self.processor.set("menuEnter")

    # IR Cut Filter
    def setIRCutFilter(self, mode: EnableStateEnum):
        self.systemMemories.ir_cut_filter = mode
        return self.processor.set("irCutFilter", mode.value)

    # Tally Mode
    def setTallyMode(self, mode: EnableStateEnum):
        self.systemMemories.tally_mode = mode
        return self.processor.set("tallyMode", mode.value)

    # Tally Level
    def setTallyLevel(self, level: TallyLevel):
        self.systemMemories.tally_level = level
        return self.processor.set("tallyLevel", level.value)

    # HDMI Color Space
    def setHDMIColorSpace(self, mode: HdmiColorFormatEnum):
        self.systemMemories.hdmi_color_space = mode
        return self.processor.set("hdmiColorSpace", mode.value)

    # Power On/Standby
    def setPowerState(self, mode: EnableStateEnum):
        self.systemMemories.power_state = mode
        return self.processor.set("powerOnStandby", mode.value)

    # Camera Generation
    def inquireCameraGeneration(self):
        return self.processor.inquire("systemCameraGeneration")

    # Software Version
    def inquireSoftwareVersion(self):
        return self.processor.inquire("softwareVersionInquire")


if __name__ == "__main__":
    systemMemories = SystemMemories()
    systemDictionary = VISCADICTIONARY["SystemSettings"]
    interface = SystemInterface(systemMemories, systemDictionary)

    # Test dei comandi
    print("Set IR Receive:", interface.setIRReceive(EnableStateEnum.ON))
    print("H Phase Up:", interface.hPhaseUp())
    print("H Phase Down:", interface.hPhaseDown())
    print("Set H Phase Value:", interface.setHPhaseValue(512))
    print("Set Image Flip:", interface.setImageFlip(EnableStateEnum.ON))
    print("Set Camera ID:", interface.setCameraID(0x1234))
    print("Set Menu Mode:", interface.setMenuMode(EnableStateEnum.ON))
    print("Menu Enter:", interface.menuEnter())
    print("Set IR Cut Filter:", interface.setIRCutFilter(EnableStateEnum.ON))
    print("Set Tally Mode:", interface.setTallyMode(EnableStateEnum.ON))
    print("Set Tally Level:", interface.setTallyLevel(TallyLevel.HIGH))
    print("Set HDMI Color Space:", interface.setHDMIColorSpace(HdmiColorFormatEnum.RGB))
    print("Set Power State:", interface.setPowerState(EnableStateEnum.ON))
    print("Inquire Camera Generation:", interface.inquireCameraGeneration())
    print("Inquire Software Version:", interface.inquireSoftwareVersion())
