
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.dictionary.ViscaDictionary import VISCADICTIONARY


class PresetInterface(BaseInterfaceClass):
    def __init__(self, _presetDictionary: dict):
        super().__init__()
        self.command_map = _presetDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # Reset Preset
    def resetPreset(self, preset_number: int):
        return self.processor.set("presetReset", preset_number)

    def inquireResetPreset(self):
        return self.processor.inquire("presetReset")

    # Set Preset
    def setPreset(self, preset_number: int):
        return self.processor.set("presetSet", preset_number)

    def inquireSetPreset(self):
        return self.processor.inquire("presetSet")

    # Recall Preset
    def recallPreset(self, preset_number: int):
        return self.processor.set("presetRecall", preset_number)

    def inquireRecallPreset(self):
        return self.processor.inquire("presetRecall")

    # Preset Speed Select
    def setPresetSpeedSelect(self, mode: int):
        return self.processor.set("presetSpeedSelect", mode)

    def inquirePresetSpeedSelect(self):
        return self.processor.inquire("presetSpeedSelect")

    # Preset Speed Separate
    def setPresetSpeedSeparate(self, preset_number: int, position_speed: int):
        return self.processor.set("presetSpeedSeparate", preset_number, position_speed)

    def inquirePresetSpeedSeparate(self):
        return self.processor.inquire("presetSpeedSeparate")

    # Preset Speed Common
    def setPresetSpeedCommon(self, speed: int):
        return self.processor.set("presetSpeedCommon", speed)

    def inquirePresetSpeedCommon(self):
        return self.processor.inquire("presetSpeedCommon")

    # Preset Mode
    def setPresetMode(self, mode: int):
        return self.processor.set("presetMode", mode)

    def inquirePresetMode(self):
        return self.processor.inquire("presetMode")

    # Preset Call Mode
    def setPresetCallMode(self, mode: int):
        return self.processor.set("presetCallMode", mode)

    def inquirePresetCallMode(self):
        return self.processor.inquire("presetCallMode")


if __name__ == "__main__":
    presetDictionary = VISCADICTIONARY["PresetSettings"]
    interface = PresetInterface(presetDictionary)

    # Esempi di utilizzo
    print("Reset Preset:", interface.resetPreset(1))
    print("Set Preset:", interface.setPreset(5))
    print("Recall Preset:", interface.recallPreset(10))
    print("Set Preset Speed Select:", interface.setPresetSpeedSelect(2))
    print("Set Preset Speed Separate:", interface.setPresetSpeedSeparate(10, 15))
    print("Set Preset Speed Common:", interface.setPresetSpeedCommon(10))
    print("Set Preset Mode:", interface.setPresetMode(1))
    print("Set Preset Call Mode:", interface.setPresetCallMode(3))
