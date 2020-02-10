from enum import Enum

class Segment(Enum):
    CONST = "constant"
    ARG = "argument"
    LOCAL =  "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

class Command(Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"

class JackVMWriter:
    def __init__(self):
        self.commands = []

    def write_push(self, segment, index):
        output = ["push {} {}".format(segment.value, index)]
        self.commands.append(output)
        return output

    def write_pop(self, segment, index):
        output = ["pop {} {}".format(segment.value, index)]
        self.commands.append(output)
        return output

    def write_arithmetic(self, command):
        output = ["{}".format(command.value)]
        self.commands.append(output)
        return output

    def write_label(self, label):
        output = ["label {}".format(label)]
        self.commands.append(output)
        return output

    def write_goto(self, label):
        output = ["goto {}".format(label)]
        self.commands.append(output)
        return output

    def write_if(self, label):
        output = ["if-goto {}".format(label)]
        self.commands.append(output)
        return output

    def write_call(self, name, nargs):
        output = ["call {} {}".format(name, nargs)]
        self.commands.append(output)
        return output

    def write_function(self, name, nlocals):
        output = ["function {} {}".format(name, nlocals)]
        self.commands.append(output)
        return output

    def write_return(self):
        output = ["return"]
        self.commands.append(output)
        return output

    def output(self):
        return "\n".join([y for x in self.commands for y in x])
