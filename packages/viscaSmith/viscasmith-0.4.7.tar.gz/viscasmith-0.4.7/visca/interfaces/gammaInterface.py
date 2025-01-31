from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.gammaMemories import GammaMemories

class GammaInterface(BaseInterfaceClass):
    def __init__(self, _gammaMemories: GammaMemories, _gammaDictionary: dict):
        super().__init__()
        self.gammaMemories = _gammaMemories
        self.command_map = _gammaDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # Gamma Select
    def setGammaSelect(self, mode: GammaLevelEnum):
        self._last_command = None
        self.gammaMemories.gamma_select = mode
        return self.processor.set("gammaSelect", mode.value)

    def getGammaSelect(self):
        self._last_command = "get gammaSelect"
        return self.processor.inquire("gammaSelect")

    # Gamma Pattern
    def setGammaPatternValue(self, value: int):
        if 0 < value > 200:
            raise ValueError("Valore fuori range per Gamma Pattern Value.")
        self._last_command = None
        self.gammaMemories.gamma_pattern_value = value
        return self.processor.set("gammaPatternValue", value)

    def getGammaPatternValue(self):
        self._last_command = "get gammaPatternValue"
        return self.processor.inquire("gammaPatternValue")

    # Gamma Offset
    def setGammaOffsetValue(self, polarity: GammaPolarityEnum, _width: int):
        """
        Imposta il valore di Offset per il Gamma.
        :param _width:  -64 a 64.
        :param polarity: un valore di polarità. 0 o 1.
        :param width: -64 a 64.
        :return:
        """
        if _width < -64 or _width > 64:
            raise ValueError("Valore fuori range per Gamma Offset Width.")
        self._last_command = None
        self.gammaMemories.gamma_offset_value = {"polarity": polarity, "width":_width}
        _width += 64
        return self.processor.set("gammaOffsetValue", polarity.value, _width)

    def getGammaOffsetValue(self):
        self._last_command = "get gammaOffsetValue"
        return self.processor.inquire("gammaOffsetValue")

    # Gamma Level
    def setGammaLevelValue(self, value: int):
        """
        Imposta il valore di Gamma Level.
        :param value: -7 a 7.
        :return:
        """
        if value < -7 or value > 7:
            raise ValueError("Valore fuori range per Gamma Level Value.")
        self._last_command = None
        self.gammaMemories.gamma_level_value = value
        value += 7
        return self.processor.set("gammaLevelValue", value)

    def getGammaLevelValue(self):
        self._last_command = "get gammaLevelValue"
        return self.processor.inquire("gammaLevelValue")

    # Black Gamma Level
    def setBlackGammaLevelValue(self, value: int):
        """
        Imposta il valore di Black Gamma Level.
        :param value: -7 a 7.
        :return:
        """
        if value < -7 or value > 7:
            raise ValueError("Valore fuori range per Black Gamma Level Value.")
        self._last_command = None
        self.gammaMemories.black_gamma_level_value = value
        value += 7
        return self.processor.set("blackGammaLevelValue", value)

    def getBlackGammaLevelValue(self):
        self._last_command = "get blackGammaLevelValue"
        return self.processor.inquire("blackGammaLevelValue")

    # Black Gamma Range
    def setBlackGammaRangeValue(self, mode: BlackGammaRangeEnum):
        self._last_command = None
        self.gammaMemories.black_gamma_range_value = mode
        return self.processor.set("blackGammaRangeValue", mode.value)

    def getBlackGammaRangeValue(self):
        self._last_command = "get blackGammaRangeValue"
        return self.processor.inquire("blackGammaRangeValue")

    # Black Level
    def resetBlackLevel(self):
        self._last_command = None
        self.gammaMemories.black_level_value = 0
        return self.processor.set("blackLevelReset")

    def blackLevelUp(self):
        self._last_command = None
        if self.gammaMemories.black_level_value > 60:
            self.gammaMemories.black_level_value = 60
        self.gammaMemories.black_level_value += 1

        return self.processor.set("blackLevelUp")

    def blackLevelDown(self):
        self._last_command = None
        if self.gammaMemories.black_level_value < -60:
            self.gammaMemories.black_level_value = -60
        self.gammaMemories.black_level_value -= 1
        return self.processor.set("blackLevelDown")

    def setBlackLevelValue(self, value: int):
        """
        Imposta il valore di Black Level.
        :param value: -48 a 48.
        :return:
        """
        if value < -48 or value > 48:
            raise ValueError("Valore fuori range per Black Level Value.")
        self._last_command = None
        self.gammaMemories.black_level_value = value
        value += 48
        return self.processor.set("blackLevelValue", value)

    def getBlackLevelValue(self):
        self._last_command = "get blackLevelValue"
        return self.processor.inquire("blackLevelValue")

if __name__ == "__main__":
    gammaMemories = GammaMemories()
    gammaDictionary = VISCADICTIONARY["GammaSettings"]
    gammaInterface = GammaInterface(gammaMemories, gammaDictionary)
    print(f"cmd setGammaSelect {GammaLevelEnum.STD}")
    print(gammaInterface.setGammaSelect(GammaLevelEnum.STD))
    print(f"cmd getGammaSelect")
    print(gammaInterface.getGammaSelect())
    print(f"cmd setGammaPatternValue 1")
    print(gammaInterface.setGammaPatternValue(1))
    print(f"cmd getGammaPatternValue")
    print(gammaInterface.getGammaPatternValue())
    print(f"cmd setGammaOffsetValue 1 1")
    print(gammaInterface.setGammaOffsetValue(GammaPolarityEnum.POSITIVE, 1))
    print(f"cmd getGammaOffsetValue")
    print(gammaInterface.getGammaOffsetValue())
    print(f"cmd setGammaLevelValue 1")
    print(gammaInterface.setGammaLevelValue(1))
    print(f"cmd getGammaLevelValue")
    print(gammaInterface.getGammaLevelValue())
    print(f"cmd setBlackGammaLevelValue 1")
    print(gammaInterface.setBlackGammaLevelValue(1))
    print(f"cmd getBlackGammaLevelValue")
    print(gammaInterface.getBlackGammaLevelValue())
    print(f"cmd setBlackGammaRangeValue 1")
    print(gammaInterface.setBlackGammaRangeValue(BlackGammaRangeEnum.WIDE))
    print(f"cmd getBlackGammaRangeValue")
    print(gammaInterface.getBlackGammaRangeValue())
    print(f"cmd resetBlackLevel")
    print(gammaInterface.resetBlackLevel())
    print(f"cmd increaseBlackLevel")
    print(gammaInterface.blackLevelUp())
    print(f"cmd decreaseBlackLevel")
    print(gammaInterface.blackLevelDown())
    print(f"cmd setBlackLevelValue 50")
    print(gammaInterface.setBlackLevelValue(2))
    print(f"cmd getBlackLevelValue")
    print(gammaInterface.getBlackLevelValue())
