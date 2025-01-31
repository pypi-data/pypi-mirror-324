from visca.dictionary.enumerations import *


class GenericsMemories:
    _picture_profile: PictureProfileEnum
    _high_resolution: EnableStateEnum
    _flicker_cancel: EnableStateEnum
    _image_stabilizer: EnableStateEnum

    _noise_reduction: NoiseReductionLevel
    _noise_reduction_2d_3d: dict
    _picture_effect: PictureEffectEnum
    _defog: EnableStateEnum
    _color_bar: EnableStateEnum

    def __init__(self):
        # Stato iniziale
        self._picture_profile = PictureProfileEnum.PP1
        self._high_resolution = EnableStateEnum.OFF
        self._flicker_cancel = EnableStateEnum.OFF
        self._image_stabilizer = EnableStateEnum.OFF
        self._noise_reduction = NoiseReductionLevel.WEAK
        self._noise_reduction_2d_3d = {
            "2D": NoiseReduction2DEnum.OFF,
            "3D": NoiseReduction3DEnum.OFF
        }
        self._picture_effect = PictureEffectEnum.OFF
        self._defog = EnableStateEnum.OFF
        self._color_bar = EnableStateEnum.OFF

    @property
    def pictureProfile(self):
        return self._picture_profile

    @pictureProfile.setter
    def pictureProfile(self, value: PictureProfileEnum):
        if value not in PictureProfileEnum:
            raise ValueError("Valore fuori range per Picture Profile.")
        self._picture_profile = value

    @property
    def highResolution(self):
        return self._high_resolution

    @highResolution.setter
    def highResolution(self, value: EnableStateEnum):
        self._high_resolution = value

    @property
    def imageStabilizer(self):
        return self._image_stabilizer

    @imageStabilizer.setter
    def imageStabilizer(self, value: EnableStateEnum):
        self._image_stabilizer = value

    @property
    def flickerCancel(self):
        return self._flicker_cancel

    @flickerCancel.setter
    def flickerCancel(self, value: EnableStateEnum):
        self._flicker_cancel = value

    @property
    def noiseReduction(self):
        return self._noise_reduction

    @noiseReduction.setter
    def noiseReduction(self, value: NoiseReductionLevel):
        self._noise_reduction = value

    @property
    def noiseReduction2D3D(self):
        return self._noise_reduction_2d_3d

    @noiseReduction2D3D.setter
    def noiseReduction2D3D(self, value: dict):
        self._noise_reduction_2d_3d = value

    @property
    def pictureEffect(self):
        return self._picture_effect

    @pictureEffect.setter
    def pictureEffect(self, mode: PictureEffectEnum):
        self._picture_effect = mode

    @property
    def defog(self):
        return self._defog

    @defog.setter
    def defog(self, value: EnableStateEnum):
        self._defog = value

    @property
    def colorBar(self):
        return self._color_bar

    @colorBar.setter
    def colorBar(self, value: EnableStateEnum):
        self._color_bar = value

    def serialize(self):
        return {
            "pictureProfile": self._picture_profile.name,
            "highResolution": self._high_resolution.name,
            "flickerCancel": self._flicker_cancel.name,
            "imageStabilizer": self._image_stabilizer.name,
            "noiseReduction": self._noise_reduction.name,
            "noiseReduction2D3D": {
                "2D": self._noise_reduction_2d_3d["2D"].name,
                "3D": self._noise_reduction_2d_3d["3D"].name
            },
            "pictureEffect": self._picture_effect.name,
            "defog": self._defog.name,
            "colorBar": self._color_bar.name
        }

    def deserialize(self, data):
        self._picture_profile = self.returnEnumerationFromSomething(data["pictureProfile"], PictureProfileEnum)
        self._high_resolution = self.returnEnumerationFromSomething(data["highResolution"], EnableStateEnum)
        self._flicker_cancel = self.returnEnumerationFromSomething(data["flickerCancel"], EnableStateEnum)
        self._image_stabilizer = self.returnEnumerationFromSomething(data["imageStabilizer"], EnableStateEnum)
        self._noise_reduction = self.returnEnumerationFromSomething(data["noiseReduction"], NoiseReductionLevel)
        self._noise_reduction_2d_3d = {
            "2D": self.returnEnumerationFromSomething(data["noiseReduction2D3D"]["2D"], NoiseReduction2DEnum),
            "3D": self.returnEnumerationFromSomething(data["noiseReduction2D3D"]["3D"], NoiseReduction3DEnum)
        }
        self._picture_effect = self.returnEnumerationFromSomething(data["pictureEffect"], PictureEffectEnum)
        self._defog = self.returnEnumerationFromSomething(data["defog"], EnableStateEnum)
        self._color_bar = self.returnEnumerationFromSomething(data["colorBar"], EnableStateEnum)

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
