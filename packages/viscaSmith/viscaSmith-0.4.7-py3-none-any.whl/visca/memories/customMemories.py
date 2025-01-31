from visca.dictionary.enumerations import PictureProfileEnum
from visca.interfaces.avonicInterface import *


class CustomMemories:
    _dynamicHotPixelCorrection: DynamicHotPixelCorrectionEnum
    _cameraAperture: int
    _cameraBrightness: int
    _cameraContrast: int
    _cameraFlip: CameraFlipEnum
    _cameraIridix: int
    _autoFocusZone: AutoFocusZoneEnum
    _colorHue: int
    _panTiltMaxSpeed: PanTiltStateEnum
    _presetSpeed_horizontal: int
    _presetSpeed_vertical: int
    _presetSpeed_zoom: int
    _pictureProfile: PictureProfileEnum

    def __init__(self):
        self._dynamicHotPixelCorrection = DynamicHotPixelCorrectionEnum.OFF
        self._cameraAperture = 0
        self._cameraBrightness = 0
        self._cameraContrast = 0
        self._cameraFlip = CameraFlipEnum.OFF
        self._cameraIridix = 0
        self._autoFocusZone = AutoFocusZoneEnum.FRONT_FOCUS
        self._colorHue = 0
        self._panTiltMaxSpeed = PanTiltStateEnum.OFF
        self._presetSpeed_horizontal = 0
        self._presetSpeed_vertical = 0
        self._presetSpeed_zoom = 0
        self._pictureProfile = PictureProfileEnum.PP1

    @property
    def dynamicHotPixelCorrection(self):
        return self._dynamicHotPixelCorrection

    @dynamicHotPixelCorrection.setter
    def dynamicHotPixelCorrection(self, value: DynamicHotPixelCorrectionEnum):
        self._dynamicHotPixelCorrection = value

    @property
    def cameraAperture(self):
        return self._cameraAperture

    @cameraAperture.setter
    def cameraAperture(self, value: int):
        self._cameraAperture = value

    @property
    def cameraBrightness(self):
        return self._cameraBrightness

    @cameraBrightness.setter
    def cameraBrightness(self, value: int):
        self._cameraBrightness = value

    @property
    def cameraContrast(self):
        return self._cameraContrast

    @cameraContrast.setter
    def cameraContrast(self, value: int):
        self._cameraContrast = value

    @property
    def cameraFlip(self):
        return self._cameraFlip

    @cameraFlip.setter
    def cameraFlip(self, value: CameraFlipEnum):
        self._cameraFlip = value

    @property
    def cameraIridix(self):
        return self._cameraIridix

    @cameraIridix.setter
    def cameraIridix(self, value: int):
        self._cameraIridix = value

    @property
    def autoFocusZone(self):
        return self._autoFocusZone

    @autoFocusZone.setter
    def autoFocusZone(self, value: AutoFocusZoneEnum):
        self._autoFocusZone = value

    @property
    def colorHue(self):
        return self._colorHue

    @colorHue.setter
    def colorHue(self, value: int):
        self._colorHue = value

    @property
    def panTiltMaxSpeed(self):
        return self._panTiltMaxSpeed

    @panTiltMaxSpeed.setter
    def panTiltMaxSpeed(self, value: PanTiltStateEnum):
        self._panTiltMaxSpeed = value

    @property
    def presetSpeed_horizontal(self):
        return self._presetSpeed_horizontal

    @presetSpeed_horizontal.setter
    def presetSpeed_horizontal(self, value: int):
        self._presetSpeed_horizontal = value

    @property
    def presetSpeed_vertical(self):
        return self._presetSpeed_vertical

    @presetSpeed_vertical.setter
    def presetSpeed_vertical(self, value: int):
        self._presetSpeed_vertical = value

    @property
    def presetSpeed_zoom(self):
        return self._presetSpeed_zoom

    @presetSpeed_zoom.setter
    def presetSpeed_zoom(self, value: int):
        self._presetSpeed_zoom = value

    @property
    def pictureProfile(self):
        return self._pictureProfile

    @pictureProfile.setter
    def pictureProfile(self, value: PictureProfileEnum):
        self._pictureProfile = value

    def serialize(self):
        return {
            "dynamicHotPixelCorrection": self.dynamicHotPixelCorrection,
            "cameraAperture": self.cameraAperture,
            "cameraBrightness": self.cameraBrightness,
            "cameraContrast": self.cameraContrast,
            "cameraFlip": self.cameraFlip,
            "cameraIridix": self.cameraIridix,
            "autoFocusZone": self.autoFocusZone,
            "colorHue": self.colorHue,
            "panTiltMaxSpeed": self.panTiltMaxSpeed,
            "presetSpeed_horizontal": self.presetSpeed_horizontal,
            "presetSpeed_vertical": self.presetSpeed_vertical,
            "presetSpeed_zoom": self.presetSpeed_zoom
        }

    def deserialize(self, data):
        try:
            self._dynamicHotPixelCorrection = self.returnEnumerationFromSomething(data["dynamicHotPixelCorrection"], int)
            self._cameraAperture = self.returnEnumerationFromSomething(data["cameraAperture"], int)
            self._cameraBrightness = self.returnEnumerationFromSomething(data["cameraBrightness"], int)
            self._cameraContrast = self.returnEnumerationFromSomething(data["cameraContrast"], int)
            self._cameraFlip = self.returnEnumerationFromSomething(data["cameraFlip"], int)
            self._cameraIridix = self.returnEnumerationFromSomething(data["cameraIridix"], int)
            self._autoFocusZone = self.returnEnumerationFromSomething(data["autoFocusZone"], int)
            self._colorHue = self.returnEnumerationFromSomething(data["colorHue"], int)
            self._panTiltMaxSpeed = self.returnEnumerationFromSomething(data["panTiltMaxSpeed"], PanTiltStateEnum)
            self._presetSpeed_horizontal = self.returnEnumerationFromSomething(data["presetSpeed_horizontal"], int)
            self._presetSpeed_vertical = self.returnEnumerationFromSomething(data["presetSpeed_vertical"], int)
            self._presetSpeed_zoom = self.returnEnumerationFromSomething(data["presetSpeed_zoom"], int)
        except KeyError as e:
            raise ValueError(f"Errore durante la deserializzazione di {data}: {e}")

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