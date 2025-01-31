from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.detailMemories import DetailMemories

class DetailInterface(BaseInterfaceClass):

    def __init__(self, _detailMemories: DetailMemories, _detailDictionary: dict):
        super().__init__()
        self.detailMemories = _detailMemories
        self.command_map = _detailDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # Detail Level
    def resetDetailLevel(self):
        """
        Reset Detail Level to default value 0
        :return:
        """
        self._last_command = None
        self.detailMemories.detailLevel = 0
        return self.processor.set("detailLevelReset")

    def detailUp(self):
        """
        Increase Detail Level by 1
        Il livello di dettaglio va da -7 a +7
        :return:
        """
        self._last_command = None
        if self.detailMemories.detailLevel < 7:
            self.detailMemories.detailLevel += 1
        else:
            self.detailMemories.detailLevel = 7
        return self.processor.set("detailLevelUp")

    def detailDown(self):
        self._last_command = None
        if self.detailMemories.detailLevel > -7:
            self.detailMemories.detailLevel -= 1
        else:
            self.detailMemories.detailLevel = -7
        return self.processor.set("detailLevelDown")

    def setDetailLevel(self, value: int):
        if value < -7 or value > 7:
            raise ValueError("Valore fuori range per Detail Level (-7, 7).")
        self._last_command = None
        self.detailMemories.detailLevel = value
        value = value + 7
        return self.processor.set("detailLevelValue", value)

    def getDetailLevel(self):
        self._last_command = "get detailLevelValue"
        return self.processor.inquire("detailLevelValue")

    # Detail Mode
    def setDetailMode(self, mode: EnumMode):
        """
        Set Detail Mode : MANUAL, AUTO
        :param mode:
        :return:
        """
        self._last_command = None
        self.detailMemories.detailMode = mode
        return self.processor.set("detailMode", mode.value)

    def getDetailMode(self):
        self._last_command = "get detailMode"
        return self.processor.inquire("detailMode")

    # Detail Bandwidth
    def setDetailBandwidth(self, mode: DetailBandWidthEnum):
        """
        Set Detail Bandwidth DEFAULT, LOW, MIDDLE, HIGH, WIDE
        :param value:
        :return:
        """
        self._last_command = None
        self.detailMemories.detail_bandwidth = mode
        return self.processor.set("detailBandwidth", mode.value)

    def getDetailBandwidth(self):
        self._last_command = "get detailBandwidth"
        return self.processor.inquire("detailBandwidth")

    # Detail Crispening
    def setDetailCrispening(self, value: int):
        if value < 0 or value > 7:
            raise ValueError("Valore fuori range per Detail Crispening (0-7).")
        self._last_command = None
        self.detailMemories.detail_crispening = value
        return self.processor.set("detailCrispening", value)

    def getDetailCrispening(self):
        self._last_command = "get detailCrispening"
        return self.processor.inquire("detailCrispening")

    # Detail HV Balance
    def setDetailHVBalance(self, value: int):
        if value < -2 or value > 2:
            raise ValueError("Valore fuori range per Detail HV Balance (-2 e 2).")
        self._last_command = None
        self.detailMemories.detail_hv_balance = value
        value = value + 2
        return self.processor.set("detailHvBalance", value)

    def getDetailHVBalance(self):
        self._last_command = "get detailHvBalance"
        return self.processor.inquire("detailHvBalance")

    # Detail BW Balance
    def setDetailBWBalance(self, mode: DetailBWBalanceEnum):
        self._last_command = None
        self.detailMemories.detail_bw_balance = mode
        return self.processor.set("detailBwBalance", mode.value)

    def getDetailBWBalance(self):
        self._last_command = "get detailBwBalance"
        return self.processor.inquire("detailBwBalance")

    # Detail Limit
    def setDetailLimit(self, value: int):
        if value < 0 or value > 7:
            raise ValueError("Valore fuori range per Detail Limit (0-7).")
        self._last_command = None
        self.detailMemories.detail_limit = value
        return self.processor.set("detailLimit", value)

    def getDetailLimit(self):
        self._last_command = "get detailLimit"
        return self.processor.inquire("detailLimit")

    # Detail Highlight
    def setDetailHighlight(self, value: int):
        if value < 0 or value > 4:
            raise ValueError("Valore fuori range per Detail Highlight (0-4).")
        self._last_command = None
        self.detailMemories.detail_highlight = value
        return self.processor.set("detailHighlight", value)

    def getDetailHighlight(self):
        self._last_command = "get detailHighlight"
        return self.processor.inquire("detailHighlight")

    # Detail Super Low
    def setDetailSuperLow(self, value: int):
        if value < 0 or value > 7:
            raise ValueError("Valore fuori range per Detail Super Low (0-7).")
        self._last_command = None
        self.detailMemories.detail_super_low = value
        return self.processor.set("detailSuperLow", value)

    def getDetailSuperLow(self):
        self._last_command = "get detailSuperLow"
        return self.processor.inquire("detailSuperLow")

if __name__ == "__main__":
    detailMemories = DetailMemories()
    detailDictionary = VISCADICTIONARY["DetailSettings"]
    detailInterface = DetailInterface(detailMemories, detailDictionary)
    print("Detail Interface")
    print(f"test get detail mode:       \t\t{detailInterface.getDetailMode()}")
    print(f"test get detail level:      \t\t{detailInterface.getDetailLevel()}")
    print(f"test get detail bandwidth:  \t\t{detailInterface.getDetailBandwidth()}")
    print(f"test get detail crispening: \t\t{detailInterface.getDetailCrispening()}")
    print(f"test get detail hv balance: \t\t{detailInterface.getDetailHVBalance()}")
    print(f"test get detail bw balance: \t\t{detailInterface.getDetailBWBalance()}")
    print(f"test get detail limit:      \t\t{detailInterface.getDetailLimit()}")
    print(f"test get detail highlight:  \t\t{detailInterface.getDetailHighlight()}")
    print(f"test get detail super low:  \t\t{detailInterface.getDetailSuperLow()}")

    print(f"test set detail mode:       \t\t{detailInterface.setDetailMode(EnumMode.MANUAL)}")
    print(f"test set detail level:      \t\t{detailInterface.setDetailLevel(5)}")
    print(f"test set detail bandwidth:  \t\t{detailInterface.setDetailBandwidth(DetailBandWidthEnum.HIGH)}")
    print(f"test set detail crispening: \t\t{detailInterface.setDetailCrispening(3)}")
    print(f"test set detail hv balance: \t\t{detailInterface.setDetailHVBalance(-2)}")
    print(f"test set detail bw balance: \t\t{detailInterface.setDetailBWBalance(DetailBWBalanceEnum.TYPE_1)}")
    print(f"test set detail limit:      \t\t{detailInterface.setDetailLimit(4)}")