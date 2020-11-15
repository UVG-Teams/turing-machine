"""
Logica Matematica
Maquina de Turing

18935   Jose Block
18049   Gian Luca Rivera
18676   Francisco Rosal
"""
from prettytable import PrettyTable
import json

# Referencia
# https://www.python-course.eu/turing_machine.php
class Tape(object):
    blank_symbol = "-"

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
        self.possible_states = configutations["q"]
        self.current_state = configutations["initial_state"]
        self.transition_function = configutations["transition_function"]
        self.final_states = configutations["final_states"]
        self.__tape = Tape(configutations["tape"])

    @property
    def actual_tape(self):
        return str(self.__tape)

    @property
    def is_final(self):
        return True if self.current_state in self.final_states else False

    def step(self):
        actual_bit = self.__tape[self.head_position]
        transition_index = "{},{}".format(self.current_state, actual_bit)
        if transition_index in self.transition_function \
            and self.current_state in self.possible_states:
            
            transition = self.transition_function[transition_index]
            self.current_state = transition["state"]
            self.__tape[self.head_position] = transition["value"]

            if transition["direc"] == "R":
                self.head_position += 1
            elif transition["direc"] == "L":
                self.head_position -= 1
            else:
                pass

    def run(self):
        my_table = PrettyTable(["Id", "Configuracion"])
        cont = 0
        with open('output.txt', 'w') as output_file:
            while True:
                actual_setting = ""
                for i in range(len(self.actual_tape)):
                    if self.head_position == i:
                        actual_setting += self.current_state
                    actual_setting += self.actual_tape[i]
                    if self.head_position == len(self.actual_tape) \
                        and (i + 1) == len(self.actual_tape):
                        actual_setting += self.current_state

                print(actual_setting)
                my_table.add_row([cont, actual_setting])
                output_file.write(actual_setting + "\n")

                if self.is_final: return print(my_table)
                self.step()
                cont += 1

    def read_json(self, filename):
        with open(filename) as my_json:
            return json.load(my_json)


# ==================================================================
# ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~
# ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~
# ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~   .   ~
# ==================================================================

turing = TuringMachine("input-ejemplo.json")
# turing = TuringMachine("input-aceptacion.json")
# turing = TuringMachine("input-rechazo.json")
# turing = TuringMachine("input-infinito.json")
turing.run()
