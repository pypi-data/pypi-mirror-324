import json
import logging

from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.exposureMemories import ExposureMemories


class ExposureInterface(BaseInterfaceClass):

    def __init__(self, exposureMemory: ExposureMemories, _exposureDictionary: dict):
        super().__init__()
        self.exposureMemories = exposureMemory
        self.command_map = _exposureDictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    # Exposure Mode
    def setExposureMode(self, mode: ExposureModeEnum):
        """
        Imposta la modalità di esposizione.
        [FULL AUTO]:
            l’esposizione viene regolata automaticamente agendo sul guadagno,
            sulla velocità dell’otturatore elettronico e sul diaframma.

        [MANUAL]:
                è possibile regolare manualmente guadagno, velocità dell’otturatore
                elettronico e diaframma singolarmente.

        [SHUTTER Pri]:
                è possibile regolare manualmente la velocità dell’otturatore elettronico.
                Regola automaticamente l’esposizione utilizzando il guadagno e il diaframma.

        [IRIS Pri]:
                è possibile regolare il diaframma manualmente. Regola automaticamente l’esposizione
                utilizzando il guadagno e la velocità dell’otturatore elettronico.

        Quando si seleziona una delle modalità precedenti, sono visibili le opzioni disponibili per
        la modalità selezionata tra le seguenti voci di impostazione.

        :param mode: Modalità di esposizione
        """
        self._last_command = None
        self.exposureMemories.exposureMode = mode
        return self.processor.set("exposureMode", mode.value)

    def getExposureMode(self):
        self._last_command = "get exposureMode"
        return self.processor.inquire("exposureMode")

    # Iris
    def irisReset(self):
        self._last_command = None
        self.exposureMemories.irisValue = IrisSettingsEnum.F2_0
        return self.processor.set("irisReset")

    def irisUp(self):
        self._last_command = None
        maxShutter = self.getMaxValue(IrisSettingsEnum)
        if self.exposureMemories.irisValue.value < maxShutter:
            self.exposureMemories.irisValue = IrisSettingsEnum(self.exposureMemories.irisValue.value + 1)
        else:
            self.exposureMemories.irisValue = IrisSettingsEnum.F1_8
        return self.processor.set("irisUp")

    def irisDown(self):
        self._last_command = None
        minShutter = self.getMinValue(IrisSettingsEnum)
        if self.exposureMemories.irisValue.value > minShutter:
            self.exposureMemories.irisValue = IrisSettingsEnum(self.exposureMemories.irisValue.value - 1)
        else:
            self.exposureMemories.irisValue = IrisSettingsEnum.FCLOSE
        return self.processor.set("irisDown")

    def setIrisValue(self, irisValue: IrisSettingsEnum):
        """
        Imposta l'apertura dell'iride.
        Quando [MODE] è [MANUAL] o [IRIS Pri], è possibile modificare l’impostazione del diaframma.
        Sono disponibili i valori
        [F2.0], [F2.2], [F2.4], [F2.6], [F2.8], [F3.1], [F3.4], [F3.7], [F4.0], [F4.4], [F4.8],
        [F5.2], [F5.6], [F6.2], [F6.8], [F7.3], [F8.0], [F8.7], [F9.6], [F10], [F11], [CLOSE].
        :param irisValue:  Valore dell'apertura dell'iride
        :param iris: Apertura dell'iride
        """
        self._last_command = None
        self.exposureMemories.irisValue = irisValue
        return self.processor.set("irisValue", irisValue.value)

    def getIris(self):
        self._last_command = "get irisValue"
        return self.processor.inquire("irisValue")

    # Gain
    # Reset del guadagno
    def gainReset(self):
        """
        Reimposta il guadagno al valore predefinito (0 dB).
        """
        self._last_command = None
        self.exposureMemories.gainValue = GainValueEnum.GAIN_0DB
        return self.processor.set("gainReset")

    # Incremento del guadagno
    def gainUp(self):
        """
        Aumenta il guadagno di un valore discreto (incremento di 3 dB).
        """
        self._last_command = None
        max_gain = self.getMaxValue(GainValueEnum)
        if self.exposureMemories.gainValue.value < max_gain:
            self.exposureMemories.gainValue = GainValueEnum(self.exposureMemories.gainValue.value + 1)
        else:
            self.exposureMemories.gainValue = GainValueEnum.GAIN_48DB
        return self.processor.set("gainUp")

    # Decremento del guadagno
    def gainDown(self):
        """
        Riduce il guadagno di un valore discreto (decremento di 3 dB).
        """
        self._last_command = None
        min_gain = self.getMinValue(GainValueEnum)
        if self.exposureMemories.gainValue.value > min_gain:
            self.exposureMemories.gainValue = GainValueEnum(self.exposureMemories.gainValue.value - 1)
        else:
            self.exposureMemories.gainValue = GainValueEnum.GAIN_n3DB
        return self.processor.set("gainDown")

    # Impostazione del guadagno
    def setGainValue(self, gain_value: GainValueEnum):
        """
        Imposta il valore del guadagno.
        :param gain_value: Valore del guadagno (enumerazione).
        """
        self._last_command = None
        self.exposureMemories.gainValue = gain_value
        return self.processor.set("gainValue", gain_value.value)

    # Ottenere il guadagno
    def getGain(self):
        """
        Recupera il valore corrente del guadagno.
        """
        self._last_command = "get gainValue"
        return self.processor.inquire("gainValue")

    # Modalità alta sensibilità
    def setHighSensitivity(self, enabled: EnableStateEnum):
        """
        Abilita o disabilita la modalità alta sensibilità.
        :param enabled: Stato della modalità alta sensibilità.
        """
        self._last_command = None
        self.exposureMemories.highSensitivity_mode = enabled
        return self.processor.set("highSensitivityMode", enabled.value)

    def getHighSensitivity(self):
        """
        Recupera lo stato corrente della modalità alta sensibilità.
        """
        self._last_command = "get highSensitivityMode"
        return self.processor.inquire("highSensitivityMode")

    # Limite del guadagno
    def setGainLimit(self, gain_limit: GainValueEnum):
        """
        Imposta il limite massimo del guadagno.
        :param gain_limit: Limite del guadagno (enumerazione).
        """
        self._last_command = None
        self.exposureMemories.gain_limit_value = gain_limit
        return self.processor.set("gainLimitValue", gain_limit.value)

    def getGainLimit(self):
        """
        Recupera il limite massimo del guadagno.
        """
        self._last_command = "get gainLimitValue"
        return self.processor.inquire("gainLimitValue")

    # Modalità Gain Point
    def setGainPointMode(self, enabled: EnableStateEnum):
        """
        Attiva o disattiva la modalità Gain Point.
        :param enabled: Stato della modalità Gain Point.
        """
        self._last_command = None
        self.exposureMemories.gain_point_mode = enabled
        return self.processor.set("gainPointMode", enabled.value)

    def getGainPointMode(self):
        """
        Recupera lo stato corrente della modalità Gain Point.
        """
        self._last_command = "get gainPointMode"
        return self.processor.inquire("gainPointMode")

    # Valore Gain Point
    def setGainPointValue(self, gain_point: GainValueEnum):
        """
        Imposta il valore del Gain Point.
        :param gain_point: Valore del Gain Point (enumerazione).
        """
        self._last_command = None
        self.exposureMemories.gain_point_value = gain_point
        return self.processor.set("gainPointValue", gain_point.value)

    def getGainPointValue(self):
        """
        Recupera il valore corrente del Gain Point.
        """
        self._last_command = "get gainPointValue"
        return self.processor.inquire("gainPointValue")

    # Reset Shutter
    def shutterReset(self):
        """
        Reimposta la velocità dell'otturatore al valore predefinito.
        """
        self._last_command = None
        self.exposureMemories.shutter = ShutterSpeedEnum_60.s1_60
        return self.processor.set("shutterReset")

    # Incremento Shutter
    def shutterUp(self):
        """
        Incrementa la velocità dell'otturatore.
        """
        self._last_command = None
        maxShutter = self.getMaxValue(ShutterSpeedEnum_60)
        if self.exposureMemories.shutterValue.value < maxShutter:
            self.exposureMemories.shutterValue = ShutterSpeedEnum_60(self.exposureMemories.shutterValue.value + 1)
        else:
            self.exposureMemories.shutterValue = ShutterSpeedEnum_60.s1_10000
        return self.processor.set("shutterUp")

    # Decremento Shutter
    def shutterDown(self):
        """
        Decrementa la velocità dell'otturatore.
        """
        self._last_command = None
        minShutter = self.getMinValue(ShutterSpeedEnum_60)
        if self.exposureMemories.shutterValue.value > minShutter:
            self.exposureMemories.shutterValue = ShutterSpeedEnum_60(self.exposureMemories.shutterValue.value - 1)
        else:
            self.exposureMemories.shutterValue = ShutterSpeedEnum_60.s1_1
        return self.processor.set("shutterDown")

    # Imposta Shutter
    def setShutterValue(self, shutter_speed: int):
        """
        Imposta la velocità dell'otturatore su un valore specifico.
        Controlla che il valore sia compreso tra i limiti minimo e massimo.

        Quando [MODE] è [MANUAL] o [SHUTTER Pri], consente di selezionare la velocità dell’otturatore elettronico.
        Quando il formato del segnale è 59.94 o 29.97 Sono disponibili i valori
        [1/1], [2/3], [1/2], [1/3], [1/4], [1/6], [1/8], [1/10], [1/15], [1/20], [1/30], [1/50], [1/60], [1/90],
        [1/100], [1/125], [1/180], [1/250], [1/350], [1/500], [1/725], [1/1000], [1/1500], [1/2000], [1/3000],
        [1/4000], [1/6000], [1/10000].
        Quando il formato del segnale è 50 o 25 Sono disponibili i valori
        [1/1], [2/3], [1/2], [1/3], [1/4], [1/6], [1/8], [1/12], [1/15], [1/20], [1/25], [1/30], [1/50], [1/60],
        [1/100], [1/120], [1/150], [1/215], [1/300], [1/425], [1/600], [1/1000], [1/1250], [1/1750], [1/2500],
        [1/3500], [1/6000], [1/10000].
        Quando il formato del segnale è 23.98 Sono disponibili i valori
        [1/1], [2/3], [1/2], [1/3], [1/4], [1/6], [1/8], [1/12], [1/20], [1/24], [1/25], [1/40], [1/48],
        [1/50], [1/60], [1/96], [1/100], [1/120], [1/144], [1/192], [1/200], [1/288], [1/400], [1/576],
        [1/1200], [1/2400], [1/4800], [1/10000].
        :param shutter_speed: Velocità dell'otturatore (int)
        """
        self._last_command = None
        if isinstance(shutter_speed, ShutterSpeedEnum_60):
            self.exposureMemories.shutterValue = shutter_speed
            shutter_speed = shutter_speed.value
        else:
            self.exposureMemories.shutterValue = ShutterSpeedEnum_60(shutter_speed)
        return self.processor.set("shutterValue", shutter_speed)

    # Ottieni Shutter
    def getShutter(self):
        """
        Recupera il valore corrente della velocità dell'otturatore.
        """
        self._last_command = "get shutter_value"
        return self.processor.inquire("shutterValue")

    # Imposta Max Shutter
    def setMaxShutter(self, value: ShutterSpeedEnum_60):
        """
        Imposta il valore massimo della velocità dell'otturatore.
        :param value: Valore massimo per la velocità dell'otturatore.
        """
        self._last_command = None
        self.exposureMemories.max_shutter_value = value
        return self.processor.set("maxShutterValue", value.value)

    # Ottieni Max Shutter
    def getMaxShutter(self):
        """
        Recupera il valore massimo della velocità dell'otturatore.
        """
        self._last_command = "get maxShutterValue"
        return self.processor.inquire("maxShutterValue")

    # Imposta Min Shutter
    def setMinShutter(self, value: ShutterSpeedEnum_60):
        """
        Imposta il valore minimo della velocità dell'otturatore.
        :param value: Valore minimo per la velocità dell'otturatore.
        """
        self._last_command = None
        self.exposureMemories.min_shutter_value = value
        return self.processor.set("minShutterValue", value.value)

    # Ottieni Min Shutter
    def getMinShutter(self):
        """
        Recupera il valore minimo della velocità dell'otturatore.
        """
        self._last_command = "get minShutterValue"
        return self.processor.inquire("minShutterValue")

    # AE Speed
    def setAeSpeedValue(self, ae_speed_value: int):
        """
        Imposta la velocità dell'Auto Exposure.
        Valori disponibili:
        - **1**: Standard.
        - **48**: Lenta.

        Disponibile per le modalità [FULL AUTO], [SHUTTER Pri] o [IRIS Pri].

        :param ae_speed_value: Velocità dell'AE (1-48).
        :return: Comando inviato.
        """
        if not (1 <= ae_speed_value <= 48):
            raise ValueError("Valore di AE Speed fuori dal range consentito (1-48).")
        self._last_command = None
        self.exposureMemories.ae_speed_value = ae_speed_value
        return self.processor.set("aeSpeedValue", ae_speed_value)

    def getAeSpeedValue(self):
        """
        Restituisce la velocità dell'Auto Exposure corrente.
        """
        self._last_command = "get aeSpeedValue"
        return self.processor.inquire("aeSpeedValue")

    # Auto Slow Shutter
    def setAutoSlowShutterMode(self, enabled: EnableStateEnum):
        """
        Attiva o disattiva la modalità Auto Slow Shutter.
        :param enabled: Stato (EnableStateEnum.ON / EnableStateEnum.OFF).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.auto_slow_shutter_mode = enabled
        return self.processor.set("autoSlowShutterMode", enabled.value)

    def getAutoSlowShutterMode(self):
        """
        Restituisce lo stato corrente della modalità Auto Slow Shutter.
        """
        self._last_command = "get autoSlowShutterMode"
        return self.processor.inquire("autoSlowShutterMode")

    # Exposure Compensation Mode
    def setExposureCompensationMode(self, enabled: EnableStateEnum):
        """
        Attiva o disattiva la modalità di compensazione dell'esposizione.
        :param enabled: Stato (EnableStateEnum.ON / EnableStateEnum.OFF).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.exp_comp_mode = enabled
        return self.processor.set("expCompMode", enabled.value)

    def getExposureCompensationMode(self):
        """
        Restituisce lo stato corrente della modalità di compensazione dell'esposizione.
        """
        self._last_command = "get expCompMode"
        return self.processor.inquire("expCompMode")

    # Exposure Compensation Value
    def setExposureCompensationValue(self, value: int):
        """
        Imposta il valore della compensazione dell'esposizione.
        Valori disponibili:
        - **-10**: Compensazione minima.
        - **+10**: Compensazione massima.

        :param value: Valore della compensazione dell'esposizione (-10 a 10).
        :return: Comando inviato.
        """
        if not (-10 <= value <= 10):
            raise ValueError("Valore di compensazione dell'esposizione fuori dal range consentito (-10 a 10).")
        self._last_command = None
        self.exposureMemories.exp_comp_value = value
        return self.processor.set("expCompValue", value)

    def getExposureCompensationValue(self):
        """
        Restituisce il valore corrente della compensazione dell'esposizione.
        """
        self._last_command = "get expCompValue"
        return self.processor.inquire("expCompValue")

    # Exposure Compensation Controls
    def exposureCompensationReset(self):
        """
        Reimposta il valore della compensazione dell'esposizione.
        """
        self._last_command = None
        self.exposureMemories.expCompValue = 0
        return self.processor.set("expCompReset")

    def exposureCompensationUp(self):
        """
        Incrementa il valore della compensazione dell'esposizione di 1, fino al massimo consentito (+10).
        """
        self._last_command = None
        if self.exposureMemories.expCompValue < 10:
            self.exposureMemories.expCompValue += 1
        return self.processor.set("expCompUp")

    def exposureCompensationDown(self):
        """
        Decrementa il valore della compensazione dell'esposizione di 1, fino al minimo consentito (-10).
        """
        self._last_command = None
        if self.exposureMemories.expCompValue > -10:
            self.exposureMemories.expCompValue -= 1
        return self.processor.set("expCompDown")


    # Backlight
    def setBacklightMode(self, enabled: EnableStateEnum):
        """
        Attiva o disattiva la modalità di retroilluminazione.
        Disponibile solo per alcuni scenari di esposizione.

        :param enabled: Stato ON/OFF (EnableStateEnum).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.backlight_mode = enabled
        return self.processor.set("backlightMode", enabled.value)

    def getBacklightMode(self):
        """
        Restituisce lo stato della modalità di retroilluminazione.
        """
        self._last_command = "get backlightMode"
        return self.processor.inquire("backlightMode")

    # Spotlight
    def setSpotlightMode(self, enabled: EnableStateEnum):
        """
        Attiva o disattiva la modalità spotlight.
        Ottimizza l'esposizione per soggetti molto luminosi in ambienti scuri.

        :param enabled: Stato ON/OFF (EnableStateEnum).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.spotlight_mode = enabled
        return self.processor.set("spotlightMode", enabled.value)

    def getSpotlightMode(self):
        """
        Restituisce lo stato della modalità spotlight.
        """
        self._last_command = "get spotlightMode"
        return self.processor.inquire("spotlightMode")

    # Visibility Enhancer
    def setVisibilityEnhancerMode(self, enabled: EnableStateEnum):
        """
        Attiva o disattiva il miglioramento della visibilità.

        :param enabled: Stato ON/OFF (EnableStateEnum).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.visibility_enhancer_mode = enabled
        return self.processor.set("visibilityEnhancerMode", enabled.value)

    def getVisibilityEnhancerMode(self):
        """
        Restituisce lo stato del miglioramento della visibilità.
        """
        self._last_command = "get visibility_enhancer_mode"
        return self.processor.inquire("visibilityEnhancerMode")

    def setVisibilityEnhancerLevel(self, effect_value: VisibilityEnhancerEffectLevel,
                                   brightness_compensation: VisibilityEnhancerBrightnessCompensation,
                                   compensation_value: VisibilityEnhancerCompensationLevel):
        """
        Imposta i livelli di miglioramento della visibilità.

        :param effect_value: Livello dell'effetto (0-6).
        :param brightness_compensation: Livello di compensazione della luminosità (0-3).
        :param compensation_value: Livello di compensazione (0-2).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.visibility_enhancer_level = (effect_value.value, brightness_compensation.value, compensation_value.value)
        return self.processor.set("visibilityEnhancerValues", effect_value.value, brightness_compensation.value,
                                  compensation_value.value)

    def getVisibilityEnhancerLevel(self):
        """
        Restituisce i livelli attuali di miglioramento della visibilità.
        """
        self._last_command = "get visibility_enhancer_values"
        return self.processor.inquire("visibilityEnhancerValues")

    # Low Light Bias
    def setLowLightBiasMode(self, enabled: EnableStateEnum):
        """
        Attiva o disattiva la modalità Low Light Bias.

        :param enabled: Stato ON/OFF (EnableStateEnum).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.lowLightBiasMode = enabled
        return self.processor.set("lowLightBiasMode", enabled.value)

    def getLowLightBiasMode(self):
        """
        Restituisce lo stato della modalità Low Light Bias.
        """
        self._last_command = "get lowLightBiasMode"
        return self.processor.inquire("lowLightBiasMode")

    def setLowLightBiasLevel(self, value: LowLightBiasLevel):
        """
        Imposta il livello di bias per condizioni di scarsa illuminazione.

        :param value: Livello di bias (LowLightBiasLevel).
        :return: Comando inviato.
        """
        self._last_command = None
        self.exposureMemories.lowLightBiasisValue = value
        return self.processor.set("lowLightBiasValue", value.value)

    def getLowLightBiasLevel(self):
        """
        Restituisce il livello di bias per condizioni di scarsa illuminazione.
        """
        self._last_command = "get lowLightBiasValue"
        return self.processor.inquire("lowLightBiasValue")

    def serialize(self):
        return {
            "exposureMode": self.getExposureMode(),
            "irisValue": self.getIris(),
            "gainValue": self.getGain(),
            "gainLimitValue": self.getGainLimit(),
            "gainPointMode": self.getGainPointMode(),
            "gainPointValue": self.getGainPointValue(),
            "shutterValue": self.getShutter(),
            "maxShutterValue": self.getMaxShutter(),
            "minShutterValue": self.getMinShutter(),
            "aeSpeedValue": self.getAeSpeedValue(),
            "autoSlowShutterMode": self.getAutoSlowShutterMode(),
            "expCompMode": self.getExposureCompensationMode(),
            "expCompValue": self.getExposureCompensationValue(),
            "backlightMode": self.getBacklightMode(),
            "spotlightMode": self.getSpotlightMode(),
            "visibilityEnhancerMode": self.getVisibilityEnhancerMode(),
            "visibilityEnhancerValues": self.getVisibilityEnhancerLevel(),
            "lowLightBiasMode": self.getLowLightBiasMode(),
            "lowLightBiasValue": self.getLowLightBiasLevel(),
            "highSensitivityMode": self.getHighSensitivity()
        }



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    exposureMemories = ExposureMemories()
    # stampa una lista delle funzioni
    dictionary = VISCADICTIONARY
    exposureDictionary = dictionary["ExposureSettings"]
    exposure = ExposureInterface(exposureMemories, exposureDictionary)
    print(exposure.__class__.__dict__.keys())
    print(exposure.getExposureMode())
    print(exposure.setExposureMode(ExposureModeEnum.MANUAL))
    print(exposure.getExposureMode())
    print(exposure.setExposureMode(ExposureModeEnum.FULL_AUTO))
    print(exposure.getExposureMode())
    print(exposure.getIris())
    print(exposure.setIrisValue(IrisSettingsEnum.F2_0))
    print(exposure.getIris())
    print(exposure.getGain())
    print(exposure.setGainValue(GainValueEnum.GAIN_0DB))
    print(exposure.getGain())
    print(exposure.getGainLimit())
    print(exposure.setGainLimit(GainValueEnum.GAIN_0DB))
    print(exposure.getGainLimit())
    print(exposure.getGainPointMode())
    print(exposure.setGainPointMode(EnableStateEnum.ON))
    print(exposure.getGainPointMode())
    print(exposure.getGainPointValue())
    print(exposure.setGainPointValue(GainValueEnum.GAIN_0DB))
    print(exposure.getGainPointValue())
    print(exposure.getShutter())
    print(exposure.setShutterValue(2))
    print(exposure.getShutter())
    print(exposure.getMaxShutter())
    print(exposure.setMaxShutter(ShutterSpeedEnum_60.s1_10000))
    print(exposure.getMaxShutter())
    print(exposure.getMinShutter())
    print(exposure.setMinShutter(ShutterSpeedEnum_60.s1_1))
    print(exposure.getMinShutter())
    print(exposure.getAeSpeedValue())
    print(exposure.setAeSpeedValue(1))
    print(exposure.getAeSpeedValue())
    print(exposure.getAutoSlowShutterMode())
    print(exposure.setAutoSlowShutterMode(EnableStateEnum.ON))
    print(exposure.getAutoSlowShutterMode())
    print(exposure.getExposureCompensationMode())
    print(exposure.setExposureCompensationMode(EnableStateEnum.ON))
    print(exposure.getExposureCompensationMode())
    print(exposure.getExposureCompensationValue())
    print(exposure.setExposureCompensationValue(0))
    print(exposure.getExposureCompensationValue())
    print(exposure.getBacklightMode())
    print(exposure.setBacklightMode(EnableStateEnum.ON))
    print(exposure.getBacklightMode())
    print(exposure.getSpotlightMode())
    print(exposure.setSpotlightMode(EnableStateEnum.ON))
    print(exposure.getSpotlightMode())
    print(exposure.getVisibilityEnhancerMode())
    print(exposure.setVisibilityEnhancerMode(EnableStateEnum.ON))
    print(exposure.getVisibilityEnhancerMode())
    print(exposure.getVisibilityEnhancerLevel())
    print(exposure.setVisibilityEnhancerLevel(VisibilityEnhancerEffectLevel.NORMAL,
                                              VisibilityEnhancerBrightnessCompensation.STANDARD,
                                              VisibilityEnhancerCompensationLevel.LOW))
    print(exposure.getVisibilityEnhancerLevel())
    print(exposure.getLowLightBiasMode())
    print(exposure.setLowLightBiasMode(EnableStateEnum.ON))
    print(exposure.getLowLightBiasMode())
    print(exposure.getLowLightBiasLevel())
    print(exposure.setLowLightBiasLevel(LowLightBiasLevel.LLB_04))
    print(exposure.getLowLightBiasLevel())
    print(exposure.getHighSensitivity())
    print(exposure.setHighSensitivity(EnableStateEnum.ON))
    print(exposure.getHighSensitivity())



