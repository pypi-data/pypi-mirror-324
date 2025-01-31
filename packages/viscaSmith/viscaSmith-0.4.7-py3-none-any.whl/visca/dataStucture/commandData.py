from enum import Enum


class CommandTypeEnum(Enum):
    SET = "setNoValue"
    INQUIRE = "inquire"
    SET_WITH_VALUE = "setWithValue"
    SET_WITH_VALUES = "setWithValues"

class CommandData:
    """
    Rappresenta un comando VISCA con i relativi dettagli.
    Visca non è difficile, però a causa delle molte variabili che possono essere inserite nei comandi,
    è facile fare errori. Soprattutto all'inizio metre tentavo di definire i comandi in un dizionario,
    essendo tanti e richiedendo giorni era facile cambiare un camelCase con un snake_case e un 0p con un pp. Capire
    come mai un'interfaccia funzionava e una no mi stava rallentando, quindi nel dizionario sono stati inseriti i placeholder
    come forma di doppio controllo per vedere nella fase iniziale se c'era qualche refuso nei dizionari e poi è rimasta.
    La maggior parte dei comandi VISCA ha un formato simile; c'è una intestazione che può essere 01 per il set e
    09 per il get o inquire.

    A questa segue il tipo di comando, ad esempio 04 XX per l'esposizione e ad esempio 04 39 è exposureMode, 04 0B è l'iris.
    Purtroppo i comandi non sono raggruppati per tipo, ad esempio 04 tutti i comandi per l'esposizione. Sony le raggruppa
    in categorie come Esposizione, Colore, Dettaglio Gamma etc ma poichè nel tempo sono state aggiunte funzionalità aggiuntive
    non è possibile raggrupparle in modo logico, quindi il dizionario è suddiviso con le categorie di Sony e include
    il comando specifico. L'ordine con cui sono stati scritti è lo stesso della tabella sony.

    NEl dizionario quindi ad ogni nome corrisponde una parte fissa e una parte variabile. Sony nel manuale specifica più tipi
    di placeholder per le variabili. In alcuni casi sono segnati come 0p forse per indicare che i valori non possono essere
    maggiori di 9, in altri invece indica pp. In altri forse per semplificare le tabelle usa 2p, 3p, 4p per indicare che
    che quel comando può avere un valore da 0 a 9 però deve essere preceduto da un numero. quindi se il valore è 3 e il
    placeholder è 2p diventa 23. Alcuni comandi poi possono avere più valori, in quel caso il placeholder è pp, qq, vv, ww.
    Dopo vari tentativi si è scelto di non avere un codice dinamico ma di specificare i placeholder nel dizionario, come forma
    di ulteriore controllo per evitare errori.
    La parte fissa specifica il comando ad esempio "01 04 00" e la parte variabile è il valore che si vuole
    """
    def __init__(self, name, cmd="", type_=CommandTypeEnum.SET, tip="", allowed_values=None, placeholder=None,
                 reply_format=None, inquire=None, state_value=None):
        self._name = name
        self.cmd = cmd
        self.type_ = type_
        self.tip = tip
        self.allowed_values = allowed_values or []
        self.reply_format = reply_format
        self._placeholder = placeholder or []
        self.inquire = inquire
        self.state_value = state_value

    def handle_placeholder(self, *values) -> str:
        """
        Sostituisce i placeholder nel comando con i valori forniti.
        """
        cmd = self.cmd
        value_index = 0

        # Controlla se il numero di valori coincide con il numero di placeholder specificati nella lista
        if len(values) != len(self._placeholder):
            raise ValueError("Il numero di valori non corrisponde al numero di placeholder.")

        for ph in self._placeholder:
            # Conta quanti placeholder dello stesso tipo ci sono nel comando
            placeholder_count = cmd.count(ph)


            if placeholder_count == 1:
                if ph in ["2p", "3p", "4p"]:
                    number = int(ph[0])  # Estrae il numero intero dal placeholder
                    cmd = cmd.replace(ph, f"{number}{values[value_index]}", 1)
                # Sostituisce un singolo placeholder con un valore "single byte"
                else:
                    cmd = cmd.replace(ph, self._format_single_value(values[value_index]), 1)

            elif placeholder_count == 2:
                # Gestisce "pp pp" (due byte in un unico intero)
                old_str = f"{ph} {ph}"  # es: "pp pp"
                new_str = self._format_double_value(values[value_index])
                cmd = cmd.replace(old_str, new_str, 1)

            elif placeholder_count == 3:
                # Gestisce "pp pp pp" (3 byte in un unico intero)
                # Esempio di comando: "04 AB pp pp pp"
                old_str = f"{ph} {ph} {ph}"
                new_str = self._format_triple_value(values[value_index])
                cmd = cmd.replace(old_str, new_str, 1)

            elif placeholder_count == 4:
                # Gestisce "pp pp pp pp" (4 byte in un unico intero)
                old_str = f"{ph} {ph} {ph} {ph}"
                new_str = self._format_quadruple_value(values[value_index])
                cmd = cmd.replace(old_str, new_str, 1)

            else:
                raise ValueError("Placeholder non valido o non supportato (1, 2, 3 o 4 ripetizioni).")

            value_index += 1

        return cmd

    @staticmethod
    def _format_single_value(value):
        """
        Formatta un valore singolo per un placeholder (1 byte, max 0xFF).
        """
        if value < 0x10:
            return f"0{value:X}"  # Aggiungi uno 0 davanti es: 0A
        elif value <= 0xFF:
            return f"{value:X}"
        else:
            raise ValueError("Valore singolo fuori range (max 0xFF).")

    @staticmethod
    def _format_double_value(value):
        """
        Formatta un valore doppio per un placeholder, dividendolo in 2 byte (max 0xFFFF).
        """
        if value <= 0xFFFF:
            high_byte = (value >> 8) & 0xFF
            low_byte = value & 0xFF
            return f"{high_byte:02X} {low_byte:02X}"
        else:
            raise ValueError("Valore doppio fuori range (max 0xFFFF).")

    @staticmethod
    def _format_triple_value(value):
        """
        Formatta un valore triplo (3 byte, max 0xFFFFFF).
        """
        if value <= 0xFFFFFF:
            byte1 = (value >> 16) & 0xFF
            byte2 = (value >> 8) & 0xFF
            byte3 = value & 0xFF
            return f"{byte1:02X} {byte2:02X} {byte3:02X}"
        else:
            raise ValueError("Valore triplo fuori range (max 0xFFFFFF).")

    @staticmethod
    def _format_quadruple_value(value):
        """
        Formatta un valore quadruplo (4 byte, max 0xFFFFFFFF).
        """
        if value <= 0xFFFFFFFF:
            byte1 = (value >> 24) & 0xFF
            byte2 = (value >> 16) & 0xFF
            byte3 = (value >> 8) & 0xFF
            byte4 = value & 0xFF
            return f"{byte1:02X} {byte2:02X} {byte3:02X} {byte4:02X}"
        else:
            raise ValueError("Valore quadruplo fuori range (max 0xFFFFFFFF).")

    def get_command_prefix(self) -> str:
        """
        Restituisce il prefisso del comando in base al tipo. 01 per SET, 09 per INQUIRE.
        """
        if self.type_ in {CommandTypeEnum.SET, CommandTypeEnum.SET_WITH_VALUE, CommandTypeEnum.SET_WITH_VALUES}:
            return "01"
        elif self.type_ == CommandTypeEnum.INQUIRE:
            return "09"
        return ""


import unittest

class TestCommandData(unittest.TestCase):
    def setUp(self):
        self.command1 = CommandData(
            name="test_command1",
            cmd="01 04 00 pp",
            type_=CommandTypeEnum.SET_WITH_VALUE,
            placeholder=["pp"]
        )
        self.command1a = CommandData(
            name="test_command1a",
            cmd="01 04 00 2p",
            type_=CommandTypeEnum.SET_WITH_VALUE,
            placeholder=["2p"]
        )
        self.command2 = CommandData(
            name="test_command2",
            cmd="01 04 00 pp pp",
            type_=CommandTypeEnum.SET_WITH_VALUE,
            placeholder=["pp"]
        )
        self.command3 = CommandData(
            name="test_command3",
            cmd="01 04 00 pp qq",
            type_=CommandTypeEnum.SET_WITH_VALUE,
            placeholder=["pp", "qq"]
        )
        self.command4 = CommandData(
            name="test_command4",
            cmd="01 04 00 pp qq vv ww",
            type_=CommandTypeEnum.SET_WITH_VALUE,
            placeholder=["pp", "qq", "vv", "ww"]
        )

    def test_single_placeholder_range(self):
        """
        Testa tutti i valori validi per un singolo placeholder.
        """
        for value in range(1, 256):  # Range per un singolo byte
            with self.subTest(value=value):
                cmd = self.command1.handle_placeholder(value)
                expected_cmd = f"01 04 00 {value:02X}"
                self.assertEqual(cmd, expected_cmd)
                print(f"Command: {cmd} - Expected: {expected_cmd}")

    def test_single_placeholder_range_2p(self):
        """
        Testa tutti i valori validi per un singolo placeholder (2p).
        """
        for value in range(1, 8):
            with self.subTest(value=value):
                cmd = self.command1a.handle_placeholder(value)
                expected_cmd = f"01 04 00 2{value}"
                self.assertEqual(cmd, expected_cmd)
                print(f"Command: {cmd} - Expected: {expected_cmd}")

    def test_double_placeholder_range(self):
        """
        Testa tutti i valori validi per due placeholder (es. pp pp).
        """
        for value in range(1, 65536):  # Range per due byte (16-bit)
            with self.subTest(value=value):
                cmd = self.command2.handle_placeholder(value)
                high_byte = (value >> 8) & 0xFF
                low_byte = value & 0xFF
                expected_cmd = f"01 04 00 {high_byte:02X} {low_byte:02X}"
                self.assertEqual(cmd, expected_cmd)
                print(f"Command: {cmd} - Expected: {expected_cmd}")

    def test_multiple_placeholders_range(self):
        """
        Testa combinazioni di valori validi per più placeholder.
        """
        values = [1, 2, 3, 4]  # Valori di esempio
        cmd = self.command4.handle_placeholder(*values)
        expected_cmd = "01 04 00 01 02 03 04"
        self.assertEqual(cmd, expected_cmd)
        print(f"Command: {cmd} - Expected: {expected_cmd}")

        # Testa una gamma di valori per ogni placeholder
        for p1 in range(1, 256):
            for p2 in range(1, 256):
                cmd = self.command3.handle_placeholder(p1, p2)
                expected_cmd = f"01 04 00 {p1:02X} {p2:02X}"
                self.assertEqual(cmd, expected_cmd)
                print(f"Command: {cmd} - Expected: {expected_cmd}")

if __name__ == "__main__":
    unittest.main()


