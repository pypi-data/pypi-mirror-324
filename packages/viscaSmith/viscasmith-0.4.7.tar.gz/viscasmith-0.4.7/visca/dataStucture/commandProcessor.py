from visca.dataStucture.commandData import CommandData, CommandTypeEnum


class CommandProcessor:
    """
    Command Processor serve a creare un comando Visca formattato
    in modo che continui a essere friendly human readable. Nel Dizionario
    dei command_map sono definiti dei placeholder tipo pp, 2p, 3p, qq, vv, ww
    che vengono sostituiti con i valori forniti. Questa classe quindi è una classe helper
    che si occupa di formattare i comandi in base ai placeholder definiti.
    Se il comando è "04 00 00 pp", il metodo set("setCmdTest1", 3) restituirà
    "01 04 00 00 03".
    La classe Processor usa la classe commandData come helper per formattare i comandi.
    E' stato deciso di non avere una classe mastodontica che si occupa di tutto, ma
    di avere classi più piccole che svolgono compiti specifici per migliorare manutenibilità
    e leggibilità.
    """
    def __init__(self, command_data):
        self.commands = {}
        for name, details in command_data.items():
            self.commands[name] = CommandData(
                name=name,
                cmd=details["cmd"],
                type_=CommandTypeEnum(details["type"]),
                placeholder=details.get("placeholder", []),
                tip=details.get("tip", ""),
                allowed_values=details.get("allowed_values", []),
                inquire=details.get("inquire", None),
                state_value=details.get("state", None)
            )

    def set(self, command_name, *values):
        """
        Genera un comando formattato in base al nome e ai valori forniti.
        """
        if command_name not in self.commands:
            raise ValueError(f"Comando sconosciuto: {command_name}")

        command = self.commands[command_name]
        base_cmd = command.handle_placeholder(*values)
        prefix = command.get_command_prefix()

        return f"{prefix} {base_cmd}"

    def inquire(self, command_name):
        if command_name not in self.commands:
            print(f"Comando sconosciuto: {command_name} | Comandi disponibili: {self.commands.keys()}")
            raise ValueError(f"Comando sconosciuto: {command_name}")
        command = self.commands[command_name]

        if not command.inquire:
            return
        return f"09 {command.inquire}"


import unittest

class TestCommandProcessor(unittest.TestCase):
    def setUp(self):
        # Dizionario di test
        self.dictionary = {
            "setCmdTest1": {
                "cmd": "04 00 00 pp",
                "type": "setWithValue",
                "tip": "Imposta la modalità di test",
                "allowed_values": list(range(0, 256)),
                "reply_format": "pp",
                "placeholder": ["pp"],
                "state": "exposure_mode"
            },
            "setCmdTest1a": {
                "cmd": "04 00 00 2p",
                "type": "setWithValue",
                "tip": "Imposta la modalità di test",
                "allowed_values": list(range(0, 256)),
                "reply_format": "2p",
                "placeholder": ["2p"],
                "state": "exposure_mode"
            },
            "setCmdTest2": {
                "cmd": "04 00 00 pp pp",
                "type": "setWithValue",
                "tip": "Imposta la modalità di test",
                "allowed_values": list(range(0, 256)),
                "reply_format": "pp",
                "placeholder": ["pp"],
                "state": "exposure_mode"
            },
            "setCmdTest3": {
                "cmd": "04 00 00 pp qq",
                "type": "setWithValues",
                "tip": "Imposta la modalità di test",
                "allowed_values": list(range(0, 256)),
                "reply_format": "pp qq",
                "placeholder": ["pp", "qq"],
                "state": "exposure_mode"
            },
            "setCmdTest4": {
                "cmd": "04 00 00 pp qq vv ww",
                "type": "setWithValues",
                "tip": "Imposta la modalità di test",
                "allowed_values": list(range(0, 256)),
                "reply_format": "pp qq vv ww",
                "placeholder": ["pp", "qq", "vv", "ww"],
                "state": "exposure_mode"
            }
        }

        # Inizializza il CommandProcessor
        self.processor = CommandProcessor(self.dictionary)

    def test_setCmdTest1_single_value(self):
        """Testa placeholder singolo, valore < 0x10."""
        cmd = self.processor.set("setCmdTest1", 0x0F)
        expected = "01 04 00 00 0F"
        self.assertEqual(cmd, expected)
        print(f"[test_setCmdTest1_single_value] CMD: {cmd} | Expected: {expected}")

    def test_setCmdTest1a_single_value(self):
        """Testa placeholder singolo, valore < 0x10."""
        cmd = self.processor.set("setCmdTest1a", 1)
        expected = "01 04 00 00 21"
        self.assertEqual(cmd, expected)
        print(f"[test_setCmdTest1a_single_value] CMD: {cmd} | Expected: {expected}")

    def test_setCmdTest1_single_value_over_0x10(self):
        """Testa placeholder singolo, valore >= 0x10."""
        cmd = self.processor.set("setCmdTest1", 0x1A)
        expected = "01 04 00 00 1A"
        self.assertEqual(cmd, expected)
        print(f"[test_setCmdTest1_single_value_over_0x10] CMD: {cmd} | Expected: {expected}")

    def test_setCmdTest2_double_value(self):
        """Testa placeholder con due byte ('pp pp')."""
        cmd = self.processor.set("setCmdTest2", 0x0102)
        expected = "01 04 00 00 01 02"
        self.assertEqual(cmd, expected)
        print(f"[test_setCmdTest2_double_value] CMD: {cmd} | Expected: {expected}")

    def test_setCmdTest3_two_placeholders(self):
        """Testa comando con due placeholder separati (pp e qq)."""
        cmd = self.processor.set("setCmdTest3", 0x0A, 0x0B)
        expected = "01 04 00 00 0A 0B"
        self.assertEqual(cmd, expected)
        print(f"[test_setCmdTest3_two_placeholders] CMD: {cmd} | Expected: {expected}")

    def test_setCmdTest4_four_placeholders(self):
        """Testa comando con 4 placeholder distinti: (pp, qq, vv, ww)."""
        cmd = self.processor.set("setCmdTest4", 0x01, 0x02, 0x0A, 0x0B)
        expected = "01 04 00 00 01 02 0A 0B"
        self.assertEqual(cmd, expected)
        print(f"[test_setCmdTest4_four_placeholders] CMD: {cmd} | Expected: {expected}")

    def test_unknown_command(self):
        """Verifica errore con comando inesistente."""
        with self.assertRaises(ValueError):
            self.processor.set("nonEsiste", 0x10)
        print("[test_unknown_command] Errore previsto per comando inesistente.")

    def test_wrong_number_of_values(self):
        """
        Verifica che passi il numero corretto di valori.
        Se CommandData prevede 1 placeholder, ma ne passiamo 2,
        dovrebbe lanciare un errore (IndexError o ValueError).
        """
        with self.assertRaises(ValueError):
            self.processor.set("setCmdTest1", 0x10, 0x20)
        print("[test_wrong_number_of_values] Errore previsto per numero valori errato.")


if __name__ == "__main__":
    unittest.main()
