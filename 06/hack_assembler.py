# simplest case: takes a single line and convert it to binary
import sys
import re

# 15 bit addresses
predefined_symbols = {
    'THAT': '000000000000100',
    'R14': '000000000001110',
    'R15': '000000000001111',
    'R12': '000000000001100',
    'R13': '000000000001101',
    'R10': '000000000001010',
    'R11': '000000000001011',
    'KBD': '110000000000000',
    'R4': '000000000000100',
    'R5': '000000000000101',
    'R6': '000000000000110',
    'R7': '000000000000111',
    'R0': '000000000000000',
    'R1': '000000000000001',
    'R2': '000000000000010',
    'R3': '000000000000011',
    'SCREEN': '100000000000000',
    'R8': '000000000001000',
    'R9': '000000000001001',
    'THIS': '000000000000011',
    'SP': '000000000000000',
    'ARG': '000000000000010',
    'LCL': '000000000000001'
}
comp_map = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}
dest_map = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}
jump_map = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def assemble(file_name):
    lines = read_lines(file_name)
    instruction_lines, symbols = instruction_lines_with_symbol_table(lines)
    parse_a_instruction = a_instruction_parser(16)
    result = [parse_line(line, symbols, parse_a_instruction) for line in instruction_lines]
    return "\n".join([x for x in result])

def read_lines(filename):
    with open(filename, 'r') as f:
       contents = f.read()
       return contents.split('\n')

def instruction_lines_with_symbol_table(lines):
    symbols = {}
    instruction_lines = []
    current_line = 0
    for line in lines: 
        if contains_comment(line) or is_empty(line):
           continue
        if match_a_instruction(line): 
            current_line += 1 
            instruction_lines.append((line, 'A'))
        elif match_c_instruction(line):
            current_line +=1 
            instruction_lines.append((line, 'C'))
        elif is_label(line):
            label = parse_label(line)
            symbols[label] = decimal_to_binary(current_line, count=15)
    return (instruction_lines, symbols)

def parse_line(instruction_line, symbols, parse_a_instruction):
   instruction, instruction_type = instruction_line
   instruction = instruction.strip()
   if instruction_type == 'A':
      return parse_a_instruction(instruction, symbols)
   elif instruction_type == 'C':
      return parse_c_instruction(instruction)

def is_label(line):
    return "(" in line and ")" in line

def is_empty(line):
    return not line.strip()

def contains_comment(line):
    return "//" in line

def match_c_instruction(line):
    return "=" in line or ";" in line

def match_a_instruction(line):
    return "@" in line

def parse_label(line):
    return line.replace("(", "").replace(")", "").strip()

def a_instruction_parser(base_register):
    variable_symbols = {}
    def parse_a_instruction(line, symbols):
        nonlocal base_register
        value = line[1:].strip()
        if value in predefined_symbols: 
            return "{}{}".format("0", predefined_symbols[value])
        if value in variable_symbols:
            return "{}{}".format("0", variable_symbols[value])
        try: 
            numeric_value = int(value)
            return "{}{}".format("0", decimal_to_binary(int(value), count=15))
        except ValueError as e:
            if symbols.get(value):
                return "{}{}".format("0", symbols[value])
            else:
                address = decimal_to_binary(base_register, count=15)
                variable_symbols[value] = address
                base_register += 1
                return "{}{}".format("0", address)
    return parse_a_instruction

def parse_c_instruction(line):
    dest, jump = "", ""
    comp = line.split("=").pop().split(";")[0].strip()
    if "=" in line: 
        dest = line.split("=")[0].strip()
    if ";" in line: 
        jump = line.split(";").pop().strip()
    return "111" + comp_map.get(comp, "0000000") + dest_map.get(dest, "000") + jump_map.get(jump, "000")
   
def decimal_to_binary(decimal_value, count=16):
    value = decimal_value 
    final_value = ""
    while value != 0:
        if value % 2 == 0:
            final_value = "0" + final_value
        else:
            final_value = "1" + final_value
        value = value // 2
    return final_value.rjust(16, "0")

if __name__ == '__main__': 
    if len(sys.argv) < 3:
        raise Exception("You need to supply a hack asm file and target")
    file_name = sys.argv[1]
    target_name = sys.argv[2]
    output = assemble(file_name)
    with open(target_name, "w") as f:
        f.write(output)
