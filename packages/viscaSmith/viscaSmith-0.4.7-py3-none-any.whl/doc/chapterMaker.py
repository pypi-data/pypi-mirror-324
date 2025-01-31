import inspect

from visca.dictionary.dictionaries import systemDictionary
from visca.interfaces.systemInterface import SystemInterface
from visca.memories.systemMemories import SystemMemories

# stampa i metodi della classe



memories = SystemMemories
dictionary = systemDictionary
interface = SystemInterface(memories, dictionary)
"""for n in a:
    # se nel dizionario è un type: setWithValue
    # cerca il
    print(f"Method: {n}()")
    print(getattr(color, n).__doc__)
    print('-----------------')"""

methods = dir(interface)
filter1 = [m for m in methods if not m.startswith('_')]
filter2 = [m for m in filter1 if  m.startswith('get') or m.startswith('set')]
method_order = filter2
print(method_order)

class MDFileCreator:
    """
    Classe che crea un file markdown con la documentazione delle classi.
    """
    def __init__(self, class_name, class_Interface, class_Dictionary, method_order=None):
        self.class_Interface = class_Interface
        self.class_Dictionary = class_Dictionary
        self.class_name = class_name
        self.method_order = method_order or []
        self.generate_documentation_md(self.class_Interface, self.class_Dictionary, f"{self.class_name}_documentation.md")

    @staticmethod
    def method_to_dict_key(method_name):
        """
        Converte il nome di un metodo nel formato della chiave del dizionario.
        Esempio: setBlackGammaLevelValue -> black_gamma_level_value
        """
        import re
        return re.sub(r'(?<!^)(?=[A-Z])', '_', method_name).lower()

    def generate_documentation_md(self, cls, command_dict, filename="color_documentation.md"):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("# Documentazione dei Comandi\n\n")

            methods = {name: func for name, func in inspect.getmembers(cls, predicate=inspect.isfunction)}

            if not methods:
                print("Nessun metodo trovato nella classe!")
                return

            # Usa l'ordine personalizzato, se disponibile
            for method_name in self.method_order:
                method = methods.get(method_name)

                # Trova il nome chiave nel dizionario (se esiste)
                dict_key = self.method_to_dict_key(method_name)
                command_info = command_dict.get(dict_key)

                print(f"Scrivendo documentazione per: {method_name} (Dizionario: {dict_key})")

                # Scrivi la sezione per il metodo
                file.write(f"### **{method_name}**\n\n")
                file.write(f"{method.__doc__ or '_Nessuna documentazione disponibile._'}\n\n")

                # Se il comando è presente nel dizionario, aggiungi dettagli
                if command_info:
                    file.write(f"- **Comando Visca**: `{command_info['cmd']}`\n")
                    file.write(f"- **Tip**: {command_info['tip']}\n")
                    file.write("\n")
                else:
                    file.write("_Nessun dettaglio aggiuntivo disponibile._\n\n")

                # Aggiungi separatore per la prossima funzione
                file.write("---\n\n")


# Creazione del file di documentazione
MDFileCreator("Generics", interface, dictionary, method_order)
