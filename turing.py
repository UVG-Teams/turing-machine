"""
Logica Matematica
Maquina de Turing

18935   Jose Block
18049   Gian Luca Rivera
18676   Francisco Rosal
"""
from prettytable import PrettyTable
import json

class Tape(object):
    blank_symbol = " "

    def __init__(self, tape_string):
        self.tape = dict((enumerate(tape_string)))

    def __str__(self):
        s = ""
        for i in self.tape:
            s += self.tape[i]
        return s

    def __getitem__(self, index):
        return self.tape[index] if index in self.tape else Tape.blank_symbol

    def __setitem__(self, pos, char):
        self.tape[pos] = char


class TuringMachine(object):

    def __init__(self, filename):
        self.head_position = 0
        self.import_tape(filename)

    def import_tape(self, filename):
        configutations = self.read_json(filename)
        self.__tape = Tape(configutations["tape"])
        self.current_state = configutations["initial_state"]
        self.final_states = configutations["final_states"]
        self.transition_function = configutations["transition_function"]

    @property
    def actual_tape(self):
        return str(self.__tape)

    @property
    def is_final(self):
        return True if self.current_state in self.final_states else False

    def step(self):
        actual_bit = self.__tape[self.head_position]
        if self.transition_function[actual_bit]:
            transition = self.transition_function[actual_bit]
            self.current_state = transition["state"]
            self.__tape[self.head_position] = transition["value"]

            if transition["dir"] == "R":
                self.head_position += 1
            elif transition["dir"] == "L":
                self.head_position -= 1
            else:
                pass

    def run(self):
        my_table = PrettyTable(["Id", "Estado", "Tape"])
        cont = 0
        while True:
            my_table.add_row([cont, self.current_state, self.actual_tape])
            if self.is_final: return print(my_table)
            self.step()
            cont += 1

    def read_json(self, filename):
        with open(filename) as my_json:
            content = json.load(my_json)
            return content




# ==================================================================
# ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~ 
# ==================================================================

# turing = TuringMachine("input-aceptacion.json")
# turing = TuringMachine("input-rechazo.json")
turing = TuringMachine("input-infinito.json")
turing.run()

"""
b. dise;ar maquina de turing

c. configuracion que llegue a aceptacion
d. archivo de salida de configuraciones

e. configuracion que llegue a rechazo
f. archivo de salida de configuraciones

g. configuracion que llegue a ciclo infinito
h. archivo de salida de configuraciones


Configuracion de salida:
estado actual
ubicacion de la cabeza actual
"""