from visca.dictionary.ViscaDictionary import VISCADICTIONARY
from visca.dictionary.enumerations import ExposureModeEnum, IrisSettingsEnum
from visca.memories.colorMemories import ColorMemories
from visca.memories.customMemories import CustomMemories
from visca.memories.detailMemories import DetailMemories
from visca.memories.exposureMemories import ExposureMemories
from visca.memories.focusMemories import FocusMemories
from visca.memories.gammaMemories import GammaMemories
from visca.memories.genericsMemories import GenericsMemories
from visca.memories.kneeMemories import KneeMemories
from visca.memories.panTiltMemories import PanTiltMemories
from visca.memories.systemMemories import SystemMemories
from visca.memories.zoomMemories import ZoomMemories
from visca.interfaces.colorInterface import ColorInterface
from visca.interfaces.avonicInterface import CustomInterface
from visca.interfaces.detailIInterface import DetailInterface
from visca.interfaces.exposureInterface import ExposureInterface
from visca.interfaces.focusInterface import FocusInterface
from visca.interfaces.gammaInterface import GammaInterface
from visca.interfaces.genericsInterface import GenericsInterface
from visca.interfaces.kneeInterface import KneeInterface
from visca.interfaces.panTiltInterface import PanTiltInterface
from visca.interfaces.presetInterface import PresetInterface
from visca.interfaces.systemInterface import SystemInterface
from visca.interfaces.zoomInterface import ZoomInterface


class CameraObject:
    exposureMemories: ExposureMemories
    exposure: ExposureInterface
    colorMemories: ColorMemories
    detailMemories: DetailMemories
    kneeMemories: KneeMemories
    gammaMemories: GammaMemories
    genericsMemories: GenericsMemories
    focusMemories: FocusMemories
    zoomMemories: ZoomMemories
    panTiltMemories: PanTiltMemories
    systemMemories: SystemMemories
    customMemories: CustomMemories

    # Interfaces
    exposure: ExposureInterface
    color: ColorInterface
    detail: DetailInterface
    knee: KneeInterface
    gamma: GammaInterface
    generics: GenericsInterface
    focus: FocusInterface
    zoom: ZoomInterface
    panTilt: PanTiltInterface
    system: SystemInterface
    custom: CustomInterface
    preset: PresetInterface

    """
    Oggetto camera che mantiene i dati della camera.
    """
    def __init__(self):
        self.defaultDictionary = VISCADICTIONARY
        self.initMemories()
        self.initInterfaces()

    def initMemories(self):
        self.exposureMemories = ExposureMemories()
        self.colorMemories = ColorMemories()
        self.detailMemories = DetailMemories()
        self.kneeMemories = KneeMemories()
        self.gammaMemories = GammaMemories()
        self.genericsMemories = GenericsMemories()
        self.focusMemories = FocusMemories()
        self.zoomMemories = ZoomMemories()
        self.panTiltMemories = PanTiltMemories()
        self.systemMemories = SystemMemories()
        self.customMemories = CustomMemories()

    def initInterfaces(self):
        self.exposure = ExposureInterface(self.exposureMemories, self.defaultDictionary["ExposureSettings"])
        self.color = ColorInterface(self.colorMemories, self.defaultDictionary["ColorSettings"])
        self.detail = DetailInterface(self.detailMemories, self.defaultDictionary["DetailSettings"])
        self.knee = KneeInterface(self.kneeMemories, self.defaultDictionary["KneeSettings"])
        self.gamma = GammaInterface(self.gammaMemories, self.defaultDictionary["GammaSettings"])
        self.generics = GenericsInterface(self.genericsMemories, self.defaultDictionary["GenericsSettings"])
        self.focus = FocusInterface(self.focusMemories, self.defaultDictionary["FocusSettings"])
        self.zoom = ZoomInterface(self.zoomMemories, self.defaultDictionary["ZoomSettings"])
        self.panTilt = PanTiltInterface(self.panTiltMemories, self.defaultDictionary["PanTiltSettings"])
        self.system = SystemInterface(self.systemMemories, self.defaultDictionary["SystemSettings"])
        self.custom = CustomInterface(self.customMemories, self.defaultDictionary["CustomSettings"])
        self.preset = PresetInterface(self.defaultDictionary["PresetSettings"])

    def handleSet(self, payload) -> bool:
        """
        Gestisce un comando di tipo "set".
        :param payload: Payload del comando senza terminatore.
        :return: True se il comando è stato gestito correttamente, altrimenti False.
        """
        command_payload = payload[:3]  # Prendo i primi 3 byte come base di ricerca

        print(f"Comando Payload: {command_payload.hex()}")

        command_found = False

        for category, commands in self.defaultDictionary.items():
            for command_name, details in commands.items():
                command_base = details["cmd"]
                placeholders = details.get("placeholder", [])

                # Rimuove i placeholder per il confronto iniziale
                base_cmd_hex = command_base.split("pp")[0]  # Prendi solo la parte fissa prima dei placeholder
                base_cmd_bytes = bytes.fromhex(base_cmd_hex.replace(" ", ""))

                if command_payload.startswith(base_cmd_bytes):  # Controlla solo la parte base del comando
                    print(f"✅ Comando trovato: {command_name} -> {details['cmd']}")

                    # Rimuove la parte fissa dal payload ricevuto per analizzare i valori dinamici
                    dynamic_values = payload[len(base_cmd_bytes):]

                    if not dynamic_values:
                        raise ValueError(f"\t❌ ERRORE: Nessun valore dinamico in {payload.hex()} per {command_name}")

                    # Se ha placeholder, prova a estrarre i valori
                    if placeholders and details.get("allowed_values"):
                        try:
                            value = int(dynamic_values.hex(), 16)
                        except ValueError:
                            raise ValueError(
                                f"\t❌ ERRORE: Conversione fallita per {dynamic_values.hex()} in {command_name}")

                        if value not in details["allowed_values"]:
                            print(f"\t❌ Valore {value} non valido per {command_name}!")
                            return False

                        return self.setMemories(category, command_name, value)

                    command_found = True  # Segnalo che almeno un comando è stato trovato

        if not command_found:
            print(f"\t❌ Comando non trovato. Payload rimanente: {command_payload.hex()}")
            raise NotImplementedError(f"Comando non trovato: {command_payload.hex()}")

        return False  # Default in caso di errore

    def setMemories(self, category, memory, value) -> bool:
        """
        Imposta un valore in una memoria specifica.
        :param category: Categoria (es. "Exposure")
        :param memory: Nome della memoria (es. "exposure_mode")
        :param value: Valore da impostare
        :return: True se l'operazione è riuscita, altrimenti False.
        """
        # Mappa le categorie alle classi di memoria
        memories = {
            "ExposureSettings": self.exposure.exposureMemories,
            "ColorSettings": self.color.colorMemories,
            "DetailSettings": self.detail.detailMemories,
            "KneeSettings": self.knee.kneeMemories,
            "GammaSettings": self.gamma.gammaMemories,
            "GenericsSettings": self.generics.genericsMemories,
            "FocusSettings": self.focus.focusMemories,
            "ZoomSettings": self.zoom.zoomMemories,
            "PanTiltSettings": self.panTilt.panTiltMemories,
            "SystemSettings": self.system.systemMemories,
            "CustomSettings": self.custom.customMemories,
        }
        # Ottieni la memoria corrispondente alla categoria
        memory_object = memories.get(category)
        if not memory_object:
            print(f"Categoria '{category}' non trovata.")
            return False

        # Verifica se la memoria esiste nella classe corrispondente
        if not hasattr(memory_object, memory):
            print(f"Memoria '{memory}' non trovata nella categoria '{category}'.")
            return False

        # Imposta il valore nella memoria
        setattr(memory_object, memory, value)
        print(f"Impostato {memory} in {category} a {value}.")
        return True


if __name__ == '__main__':
    camera = CameraObject()
    print(camera.exposure.setExposureMode(ExposureModeEnum.MANUAL))
    print(camera.exposure.getExposureMode())

    print(camera.exposure.setIrisValue(IrisSettingsEnum.F1_8))
