import logging


from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import *
from visca.dataStucture.commandProcessor import CommandProcessor
from visca.memories.colorMemories import ColorMemories
from visca.baseClasses.baseInterfaceClass import BaseInterfaceClass



class ColorInterface(BaseInterfaceClass):

    def __init__(self, _colorMemories: ColorMemories, _commandMap: dict):
        super().__init__()
        self.colorMemories = _colorMemories
        self.command_map = _commandMap
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setDictionary(self, dictionary):
        self.command_map = dictionary
        self.processor = CommandProcessor(self.command_map)
        self.setup()

    def setWhiteBalanceMode(self, mode: WhiteBalanceModeEnum):
        """
        Seleziona la modalità di bilanciamento del bianco.

        Modalità disponibili:
        - **AUTO1**: Regola automaticamente il colore per avvicinarlo
          all'immagine visualizzata.
        - **AUTO2**: Regola automaticamente il bilanciamento del bianco
          per riprodurre i colori originali degli oggetti, eliminando le
          influenze dell’illuminazione ambiente.
        - **INDOOR**: Fissa R/B GAIN a una temperatura di colore di 3200 K.
        - **OUTDOOR**: Fissa R/B GAIN a una temperatura di colore di 5800 K.
        - **ONE PUSH**: Regola il bilanciamento del bianco al momento
          della pressione di specifici pulsanti (ad esempio, il pulsante
          HOME del telecomando o il pulsante ONE PUSH AWB del joystick)
          mentre si inquadra un soggetto bianco di grandi dimensioni.
        - **MANUAL**: Permette la regolazione manuale del bilanciamento
          del bianco.

        :param mode: Modalità di bilanciamento del bianco (WhiteBalanceModeEnum).
        :return: Comando inviato al processore.
        """
        self._last_command = None
        self.colorMemories.whiteBalanceMode = mode
        return self.processor.set("whiteBalanceMode", mode.value)

    def getWhiteBalanceMode(self):
        self._last_command = "get whiteBalanceMode"
        return self.processor.inquire("whiteBalanceMode")

    def onePushTrigger(self):
        self._last_command = None
        return self.processor.set("onePushTrigger")

    def setWBSpeed(self, value: int):
        """
        Imposta la velocità di convergenza del bilanciamento del bianco.

        Valori disponibili:
        - **1**: Lento.
        - **5**: Veloce.

        Questa impostazione è valida solo per le modalità AUTO1 e AUTO2.

        :param value: Velocità del bilanciamento del bianco (1-5).
        :return: Comando inviato.
        """
        self._last_command = None
        self.colorMemories.wbSpeed = value
        return self.processor.set("wbSpeed", value)

    def getWBSpeed(self):
        self._last_command = "get wbSpeed"
        return self.processor.inquire("wbSpeed")

    def setOffset(self, value : int):
        """
            Sposta il punto di convergenza del bilanciamento del bianco.

            Valori disponibili:
            - **-7**: Spostamento massimo verso il blu.
            - **+7**: Spostamento massimo verso il rosso.

            Applicabile alle modalità AUTO1, AUTO2 e ONE PUSH.

            :param value: Offset per il bilanciamento del bianco (0 a 14).
            :return: Comando inviato.
            """
        if value < -7 or value > 7:
            raise ValueError("Valore fuori range per setOffset secondo lo standard VISCA.")
        self._last_command = None
        self.colorMemories.offsetValue = value
        value = value + 7
        return self.processor.set("offsetValue", value)

    def getOffset(self):
        self._last_command = "get offsetValue"
        return self.processor.inquire("offsetValue")

    def setRGainReset(self):
        self._last_command = None
        self.colorMemories.rGain = 80
        return self.processor.set("rGainReset")

    def setRGainUp(self):
        self._last_command = None
        if self.colorMemories.rGain < 127:
            self.colorMemories.rGain += 1
        else:
            self.colorMemories.rGain = 127
        return self.processor.set("rGainUp")

    def setRGainDown(self):
        self._last_command = None
        if self.colorMemories.rGain > -128:
            self.colorMemories.rGain -= 1
        else:
            self.colorMemories.rGain = -128
        return self.processor.set("rGainDown")

    def setRGain(self, value: int):
        """
        Imposta manualmente il valore del Red Gain (R GAIN).

        Valori disponibili:
        - Da -128 a +127.

        Valido solo per la modalità MANUAL.

        :param value: Valore per il Red Gain.
        :return: Comando inviato.
        """
        if value < -128 or value > 127:
            raise ValueError("Valore fuori range per setRGain secondo lo standard VISCA.")

        self._last_command = None
        self.colorMemories.rGain = value
        value = value + 128
        return self.processor.set("rGainValue", value)

    def getRGain(self):
        self._last_command = "get rGainValue"
        return self.processor.inquire("rGainValue")

    def setBGainReset(self):
        self._last_command = None
        self.colorMemories.bGain = 80
        return self.processor.set("bGainReset")

    def setBGainUp(self):
        self._last_command = None
        if self.colorMemories.bGain < 127:
            self.colorMemories.bGain += 1
        else:
            self.colorMemories.bGain = 127
        return self.processor.set("bGainUp")

    def setBGainDown(self):
        self._last_command = None
        if self.colorMemories.bGain > -128:
            self.colorMemories.bGain -= 1
        else:
            self.colorMemories.bGain = -128
        return self.processor.set("bGainDown")

    def setBGain(self, value: int):
        """
        Imposta manualmente il valore del Blue Gain (B GAIN).

        Valori disponibili:
        - Da **-128** a **+127**.

        Valido solo per la modalità MANUAL.

        :param value: Valore per il Blue Gain.
        :return: Comando inviato.
        """

        if value < -128 or value > 127:
            raise ValueError("Valore fuori range per setBGain secondo lo standard VISCA.")
        self._last_command = None
        self.colorMemories.bGain = value
        value = value + 128
        return self.processor.set("bGainValue", value)

    def getBGain(self):
        self._last_command = "get bGainValue"
        return self.processor.inquire("bGainValue")

    def setChromaSuppressMode(self, mode: ChromaSuppressionEnum):
        """
        Imposta la modalità di soppressione cromatica.

        Modalità disponibili:
        - **OFF**: Soppressione cromatica disattivata.
        - **LOW**: Soppressione cromatica leggera.
        - **HIGH**: Soppressione cromatica intensa.

        :param mode: Modalità di soppressione cromatica (ChromaSuppressionEnum).
        :return: Comando inviato.
        """
        self._last_command = None
        self.colorMemories.chromaSuppression = mode
        return self.processor.set("chromaSuppress", mode.value)

    def getChromaSuppressMode(self):
        """
        Recupera la modalità attuale di soppressione cromatica.

        :return: Modalità attuale (ChromaSuppressionEnum).
        """
        self._last_command = "get chromaSuppress"
        return self.processor.inquire("chromaSuppress")

    def setMatrixMode(self, value: MatrixSelectEnum):
        """
        Seleziona una matrice preimpostata per il calcolo.

        Opzioni disponibili:
        - **STD**, **HIGH SAT**, **FL LIGHT**, **MOVIE**, **STILL**,
          **CINEMA**, **PRO**, **ITU709**, **B/W**.

        Non valido se MATRIX è impostato su OFF.

        :param value: Matrice da selezionare (MatrixSelectEnum).
        :return: Comando inviato.
        """
        self._last_command = None
        self.colorMemories.matrix = value
        return self.processor.set("matrixMode", value.value)

    def getMatrixMode(self):
        """
        Recupera la modalità attuale della matrice.

        :return: Matrice attuale (MatrixSelectEnum).
        """
        self._last_command = "get matrixMode"
        return self.processor.inquire("matrixMode")

    def setLevelReset(self):
        """
        Reimposta il livello di colore al valore predefinito (4).

        :return: Comando inviato.
        """
        self._last_command = None
        self.colorMemories.saturation = 4
        return self.processor.set("levelReset")

    def setLevelUp(self):
        """
        Incrementa il livello di colore.

        :return: Comando inviato.
        """
        self._last_command = None
        if self.colorMemories.saturation < 14:
            self.colorMemories.saturation += 1
        else:
            self.colorMemories.saturation = 14
        return self.processor.set("levelUp")

    def setLevelDown(self):
        """
        Decrementa il livello di colore.

        :return: Comando inviato.
        """
        self._last_command = None
        if self.colorMemories.saturation > 0:
            self.colorMemories.saturation -= 1
        else:
            self.colorMemories.saturation = 0
        return self.processor.set("levelDown")

    def setLevel(self, value: int):
        """
        Regola la densità del colore nell'immagine.

        Valori disponibili:
        - **0**: Colori meno densi.
        - **14**: Colori più densi.

        Non valido se MATRIX è impostato su OFF.

        :param value: Livello di densità del colore (0-14).
        :return: Comando inviato.
        """
        if value < 0 or value > 14:
            raise ValueError("Valore fuori range per setLevel secondo lo standard VISCA.")
        self._last_command = None
        self.colorMemories.saturation = value
        return self.processor.set("levelValue", value)

    def getLevel(self):
        """
        Recupera il livello attuale di densità del colore.

        :return: Livello attuale (0-14).
        """
        self._last_command = "get levelValue"
        return self.processor.inquire("levelValue")

    def setPhaseReset(self):
        """
        Reimposta la fase al valore predefinito.

        :return: Comando inviato.
        """
        self._last_command = None
        self.colorMemories.phase = 0
        return self.processor.set("phaseReset")

    def setPhaseUp(self):
        """
        Incrementa la fase.

        :return: Comando inviato.
        """
        self._last_command = None
        if self.colorMemories.phase < 7:
            self.colorMemories.phase += 1
        else:
            self.colorMemories.phase = 7
        return self.processor.set("phaseUp")

    def setPhaseDown(self):
        """
        Decrementa la fase.

        :return: Comando inviato.
        """
        self._last_command = None
        if self.colorMemories.phase > -7:
            self.colorMemories.phase -= 1
        else:
            self.colorMemories.phase = -7
        return self.processor.set("phaseDown")

    def setPhase(self, value: int):
        """
        Regola la tonalità generale del colore dell'immagine.

        Valori disponibili:
        - Da **-7** a **+7**.

        Non valido se MATRIX è impostato su OFF.

        :param value: Valore della fase (-7 a +7).
        :return: Comando inviato.
        """
        if value < -7 or value > 7:
            raise ValueError("Valore fuori range per setPhase secondo lo standard VISCA.")
        self._last_command = None
        self.colorMemories.phase = value
        value += 7
        return self.processor.set("phaseValue", value)

    def getPhase(self):
        """
        Recupera il valore attuale della fase.

        :return: Valore della fase (-7 a +7).
        """
        self._last_command = "get phaseValue"
        return self.processor.inquire("phaseValue")

    def setRG(self, value: int):
        """
        Imposta il coefficiente per la combinazione R-G.

        Valori disponibili:
        - Da -99 a +99

        Non valido se MATRIX è impostato su OFF.
        :param value: Valore del coefficiente (0-255).
        :return: Comando inviato.
        """

        self._last_command = None
        if value < -99 or value > 99:
            raise ValueError("Valore fuori range per setRG secondo lo standard VISCA.")
        self.colorMemories.rG = value
        value = value + 99
        return self.processor.set("rGValue", value)

    def getRG(self):
        self._last_command = "get rGValue"
        return self.processor.inquire("rGValue")

    def setRB(self, value: int):
        """
        Imposta il coefficiente per la combinazione R-B.

        Valori disponibili:
        - Da 0-255

        Non valido se MATRIX è impostato su OFF.

        :param value: Valore del coefficiente
        :return: Comando inviato.
        """

        self._last_command = None
        if value < -99 or value > 99:
            raise ValueError("Valore fuori range per setRB secondo lo standard")
        self.colorMemories.rB = value
        value = value + 99
        return self.processor.set("rBValue", value)

    def getRB(self):
        self._last_command = "get rBValue"
        return self.processor.inquire("rBValue")

    def setGR(self, value: int):
        """
        Imposta il coefficiente per la combinazione G-R.

        Valori disponibili:
        - Da -99 a +99

        Non valido se MATRIX è impostato su OFF.

        :param value: Valore del coefficiente
        :return: Comando inviato.
        """

        self._last_command = None
        if value < -99 or value > 99:
            raise ValueError("Valore fuori range per setGR secondo lo standard VISCA.")
        self.colorMemories.gR = value
        value = value + 99
        return self.processor.set("gRValue", value)

    def getGR(self):
        self._last_command = "get gRValue"
        return self.processor.inquire("gRValue")

    def setGB(self, value: int):
        """
        Imposta il coefficiente per la combinazione G-B.

        Valori disponibili:
        - Da -99 a +99

        Non valido se MATRIX è impostato su OFF.

        :param value: Valore del coefficiente
        :return: Comando inviato.
        """

        self._last_command = None
        if value < -99 or value > 99:
            raise ValueError("Valore fuori range per setGB secondo lo standard VISCA.")
        self.colorMemories.gB = value
        value = value + 99
        return self.processor.set("gBValue", value)

    def getGB(self):
        self._last_command = "get gBValue"
        return self.processor.inquire("gBValue")

    def setBR(self, value: int):
        """
        Imposta il coefficiente per la combinazione B-R.

        Valori disponibili:
        - Da -99 a +99

        Non valido se MATRIX è impostato su OFF.

        :param value: Valore del coefficiente
        :return: Comando inviato.
        """
        self._last_command = None
        if value < -99 or value > 99:
            raise ValueError("Valore fuori range per setBR secondo lo standard VISCA.")
        self.colorMemories.bR = value
        value = value + 99
        return self.processor.set("bRValue", value)

    def getBR(self):
        self._last_command = "get bRValue"
        return self.processor.inquire("bRValue")

    def setBG(self, value: int):
        """
        Imposta il coefficiente per la combinazione B-G.

        Valori disponibili:
        - Da -99 a +99

        Non valido se MATRIX è impostato su OFF.

        :param value: Valore del coefficiente
        :return: Comando inviato.
        """
        self._last_command = None
        if value < -99 or value > 99:
            raise ValueError("Valore fuori range per setBG secondo lo standard VISCA.")
        self.colorMemories.bG = value
        value = value + 99
        return self.processor.set("bGValue", value)

    def getBG(self):
        self._last_command = "get bGValue"
        return self.processor.inquire("bGValue")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    colorMemories = ColorMemories()
    colorDictionary = VISCADICTIONARY["ColorSettings"]
    color = ColorInterface(colorMemories, colorDictionary)

    print(color.__class__.__dict__.keys())
    print("SET WHITE BALANCE MODE")
    print(color.getWhiteBalanceMode())
    print(color.setWhiteBalanceMode(WhiteBalanceModeEnum.AUTO_1))
    print(color.getWhiteBalanceMode())
    print("ONE PUSH TRIGGER")
    print(color.onePushTrigger())
    print("RG GAIN")
    print(color.setRGainReset())
    print(color.setRGainUp())
    print(color.setRGainDown())
    print(f"RG GAIN: {color.setRGain(125)}")
    print(f"RG GAIN: {color.setRGain(50)}")

    print(color.getRGain())
    print("BG GAIN")
    print(color.setBGainReset())
    print(color.setBGainUp())
    print(color.setBGainDown())
    print(color.setBGain(125))
    print(color.getBGain())
    print("WB OFFSET")
    print(color.setOffset(2))
    print(color.getOffset())
    print("CHROMA SUPPRESS")
    print(color.setChromaSuppressMode(ChromaSuppressionEnum.WEAK))
    print(color.getChromaSuppressMode())
    print("MATRIX MODE")
    print(color.setMatrixMode(MatrixSelectEnum.STD))
    print(color.getMatrixMode())
    print("LEVEL")
    print(color.setLevelReset())
    print(color.setLevelUp())
    print(color.setLevelDown())
    print(color.setLevel(2))
    print(color.getLevel())
    print("PHASE")
    print(color.setPhaseReset())
    print(color.setPhaseUp())
    print(color.setPhaseDown())
    print(color.setPhase(2))
    print(color.getPhase())
    print("RG")
    print(color.setRG(2))
    print(color.getRG())
    print("RB")
    print(color.setRB(2))
    print(color.getRB())
    print("GR")
    print(color.setGR(2))
    print(color.getGR())
    print("GB")
    print(color.setGB(2))
    print(color.getGB())
    print("BR")
    print(color.setBR(2))
    print(color.getBR())
    print("BG")
    print(color.setBG(2))
    print(color.getBG())


