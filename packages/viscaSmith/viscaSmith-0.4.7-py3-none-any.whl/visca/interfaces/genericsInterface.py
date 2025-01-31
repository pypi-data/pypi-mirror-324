from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.genericsMemories import GenericsMemories



class GenericsInterface(BaseInterfaceClass):
    def __init__(self, _genericMemories: GenericsMemories, _genericsDictionary: dict):
        super().__init__()
        self.genericsMemories = _genericMemories
        self.command_map = _genericsDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # Picture Profile
    def setPictureProfile(self, mode: PictureProfileEnum):
        self._last_command = None
        self.genericsMemories.picture_profile = mode
        return self.processor.set("pictureProfile", mode.value)

    def getPictureProfile(self):
        self._last_command = "get pictureProfile"
        return self.processor.inquire("pictureProfile")

    # Flicker Cancel
    def setFlickerCancel(self, enableState: EnableStateEnum):
        self._last_command = None
        self.genericsMemories.flicker_cancel = enableState
        return self.processor.set("flickerCancel", enableState.value)

    def getFlickerCancel(self):
        self._last_command = "get flickerCancel"
        return self.processor.inquire("flickerCancel")

    # Image Stabilizer
    def setImageStabilizer(self, enableState: EnableStateEnum):
        self._last_command = None
        self.genericsMemories.image_stabilizer = enableState
        return self.processor.set("imageStabilizer", enableState.value)

    def getImageStabilizer(self):
        self._last_command = "get imageStabilizer"
        return self.processor.inquire("imageStabilizer")

    # Defog
    def setDefog(self, state: EnableStateEnum, level: int):
        if level not in range(0, 3):
            raise ValueError("Valore fuori range per Defog Level.")
        self._last_command = None
        self.genericsMemories.defog = {"state": state, "level": level}
        return self.processor.set("defog", state.value, level)

    def getDefog(self):
        self._last_command = "get defog"
        return self.processor.inquire("defog")

    # High Resolution
    def setHighResolution(self, mode: EnableStateEnum):
        self._last_command = None
        self.genericsMemories.high_resolution = mode
        return self.processor.set("highResolution", mode.value)

    def getHighResolution(self):
        self._last_command = "get highResolution"
        return self.processor.inquire("highResolution")

    # Noise Reduction Level
    def setNoiseReductionLevel(self, level: NoiseReductionLevel):
        """
        Imposta il livello di riduzione del rumore.
        :param level:  Livello di riduzione del rumore. Valori possibili: 0-5, 127
        :return:
        """
        if level not in NoiseReductionLevel:
            raise ValueError("Valore fuori range per Noise Reduction Level.")
        self._last_command = None
        self.genericsMemories.noise_reduction = level
        return self.processor.set("noiseReductionLevel", level.value)

    def getNoiseReductionLevel(self):
        self._last_command = "get noiseReductionLevel"
        return self.processor.inquire("noiseReductionLevel")

    # 2D/3D Noise Reduction
    def set2D3DNoiseReduction(self, nr_2d: NoiseReduction2DEnum, nr_3d: NoiseReduction3DEnum):
        """
        Imposta i livelli di riduzione del rumore 2D e 3D.
        :param nr_2d:  valori possibili: 0-5
        :param nr_3d:  valori possibili: 0-5
        :return:
        """
        self._last_command = None
        self.genericsMemories.n2D_3DNoiseReduction = {"2D": nr_2d, "3D": nr_3d}
        return self.processor.set("2d3dNr", nr_2d.value, nr_3d.value)

    def get2D3DNoiseReduction(self):
        self._last_command = "get 2d3dNr"
        return self.processor.inquire("2d3dNr")

    # Picture Effect
    def setPictureEffect(self, mode: PictureEffectEnum):
        self._last_command = None
        self.genericsMemories.picture_effect = mode
        return self.processor.set("pictureEffect", mode.value)

    def getPictureEffect(self):
        self._last_command = "get pictureEffect"
        return self.processor.inquire("pictureEffect")

    # Color Bar
    def setColorBar(self, mode: EnableStateEnum):
        self._last_command = None
        self.genericsMemories.color_bar = mode
        return self.processor.set("colorBar", mode.value)

    def getColorBar(self):
        self._last_command = "get colorBar"
        return self.processor.inquire("colorBar")


if __name__ == "__main__":
    genericMemories = GenericsMemories()
    genericsDictionary = VISCADICTIONARY["GenericsSettings"]
    interface = GenericsInterface(genericMemories, genericsDictionary)
    print(interface.setPictureProfile(PictureProfileEnum.PP2))
    print(interface.getPictureProfile())

    print(interface.setFlickerCancel(EnableStateEnum.ON))
    print(interface.getFlickerCancel())

    print(interface.setImageStabilizer(EnableStateEnum.ON))
    print(interface.getImageStabilizer())

    print(interface.setDefog(EnableStateEnum.ON, 2))
    print(interface.getDefog())

    print(interface.setHighResolution(EnableStateEnum.ON))
    print(interface.getHighResolution())

    print(interface.setNoiseReductionLevel(NoiseReductionLevel.STRONG))
    print(interface.getNoiseReductionLevel())
    print(genericMemories.noiseReduction2D3D)
    print(interface.set2D3DNoiseReduction(NoiseReduction2DEnum.NR_2, NoiseReduction3DEnum.NR_3))
    print(interface.get2D3DNoiseReduction())

    print(genericMemories.noiseReduction2D3D)
    print(interface.setPictureEffect(PictureEffectEnum.BandW))
    print(interface.getPictureEffect())

    print(interface.setColorBar(EnableStateEnum.ON))
    print(interface.getColorBar())