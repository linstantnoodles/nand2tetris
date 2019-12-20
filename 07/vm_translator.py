import sys

stack_addr = 0
local_addr = 1
arg_addr = 2
this_addr = 3
that_addr = 4
inequality_counter = {
    "gt": 0,
    "lt": 0,
    "eq": 0
}
# memory = 5-12

def read_instructions(filename):
    with open(filename, 'r') as f:
       contents = f.read()
       return [x.strip() for x in contents.split('\n') if is_instruction(x)]

def is_instruction(line):
    return line.strip() and "//" not in line

def translate(prog_name, instructions):
    parsed = [parse(prog_name, instruction) for instruction in instructions]
    return "\n".join(parsed)

def parse(prog_name, vm_instruction):
    chunked = [x.strip() for x in vm_instruction.split(" ")]
    if len(chunked) == 3:
        return parse_memory_command(prog_name, chunked)
    elif len(chunked) == 1:
        return parse_compute_command(chunked)

def parse_compute_command(vm_instruction):
    if vm_instruction[0] == "add":
        return "\n".join([
            "@{}".format(stack_addr),
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",
            "@{}".format(stack_addr),
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=M+D",
            "@{}".format(stack_addr),
            "M=M-1",
            "@temp",
            "D=M",
            "@{}".format(stack_addr),
            "A=M",
            "M=D",
            "@{}".format(stack_addr),
            "M=M+1"
        ])
    elif vm_instruction[0] == "sub":
        return "\n".join([
            "@{}".format(stack_addr),
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",
            "@{}".format(stack_addr),
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "@{}".format(stack_addr),
            "M=M-1",
            "@temp",
            "D=M",
            "@{}".format(stack_addr),
            "A=M",
            "M=D",
            "@{}".format(stack_addr),
            "M=M+1"
        ])
    elif vm_instruction[0] == "neg":
        return "\n".join([
            "@{}".format(stack_addr),
            "A=M-1",
            "D=-M",
            "M=D"
        ])
    elif vm_instruction[0] == "eq":
        inequality_counter["eq"] += 1
        idx = inequality_counter["eq"];
        return "\n".join([
            "@0",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@0",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "D=M",

            "@0",
            "M=M-1",


            "@TEMP_EQUAL.{}".format(idx),
            "D;JEQ",
            "@TEMP_NOTEQUAL.{}".format(idx),
            "D;JNE",

            "(TEMP_EQUAL.{})".format(idx),
            "@0",
            "A=M",
            "M=-1",
            "@CONTINUE_EQUAL.{}".format(idx),
            "0;JMP",

            "(TEMP_NOTEQUAL.{})".format(idx),
            "@0",
            "A=M",
            "M=0",
            "@CONTINUE_EQUAL.{}".format(idx),
            "0;JMP",

            "(CONTINUE_EQUAL.{})".format(idx),
            "@0",
            "M=M+1",
        ])
    elif vm_instruction[0] == "gt": 
        inequality_counter["gt"] += 1
        idx = inequality_counter["gt"];

        return "\n".join([
            "@0",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@0",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "D=M",

            "@0",
            "M=M-1",


            "@TEMP_GT.{}".format(idx),
            "D;JGT",
            "@TEMP_NGT.{}".format(idx),
            "D;JLE",

            "(TEMP_GT.{})".format(idx),
            "@0",
            "A=M",
            "M=-1",
            "@CONTINUE_GT.{}".format(idx),
            "0;JMP",

            "(TEMP_NGT.{})".format(idx),
            "@0",
            "A=M",
            "M=0",
            "@CONTINUE_GT.{}".format(idx),
            "0;JMP",

            "(CONTINUE_GT.{})".format(idx),
            "@0",
            "M=M+1",
        ])
    elif vm_instruction[0] == "lt": 
        inequality_counter["lt"] += 1
        idx = inequality_counter["lt"];

        return "\n".join([
            "@0",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@0",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "D=M",

            "@0",
            "M=M-1",


            "@TEMP_LT.{}".format(idx),
            "D;JLT",
            "@TEMP_NLT.{}".format(idx),
            "D;JGE",

            "(TEMP_LT.{})".format(idx),
            "@0",
            "A=M",
            "M=-1",
            "@CONTINUE_LT.{}".format(idx),
            "0;JMP",

            "(TEMP_NLT.{})".format(idx),
            "@0",
            "A=M",
            "M=0",
            "@CONTINUE_LT.{}".format(idx),
            "0;JMP",

            "(CONTINUE_LT.{})".format(idx),
            "@0",
            "M=M+1",
        ])
    elif vm_instruction[0] == "and":
        return "\n".join([
            "@{}".format(stack_addr),
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@{}".format(stack_addr),
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D&M",
            "@{}".format(stack_addr),
            "M=M-1",
            "@temp",
            "D=M",
            "@{}".format(stack_addr),
            "A=M",
            "M=D",
            "@{}".format(stack_addr),
            "M=M+1"
        ])
    elif vm_instruction[0] == "or":
        return "\n".join([
            "@{}".format(stack_addr),
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@{}".format(stack_addr),
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D|M",
            "@{}".format(stack_addr),
            "M=M-1",
            "@temp",
            "D=M",
            "@{}".format(stack_addr),
            "A=M",
            "M=D",
            "@{}".format(stack_addr),
            "M=M+1"
        ])
    elif vm_instruction[0] == "not":
        return "\n".join([
            "@{}".format(stack_addr),
            "A=M-1",
            "D=!M",
            "M=D"
        ])

def parse_memory_command(prog_name, vm_instruction):
    action, segment, value = vm_instruction 
    locations = {
        "local": 1,
        "argument": 2,
        "this": 3,
        "that": 4
    }
    if action == "push":
        if segment == "constant":
            return "\n".join([
                "@{}".format(value),
                "D=A",
                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ])
        elif segment == "static":
            return "\n".join([
                "@{}.{}".format(prog_name, value),
                "D=M",
                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ])
        elif segment in ["argument", "local", "this", "that"]:
            return "\n".join([
                "@{}".format(locations[segment]),
                "D=M",
                "@{}".format(value),
                "A=D+A",
                "D=M",
                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ])
        elif segment in ["temp"]:
            return "\n".join([
                "@5",
                "D=A",
                "@{}".format(value),
                "A=D+A",
                "D=M",
                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ])
        elif segment in ["pointer"]:
            lookup_key = "this" if value == "0" else "that"
            return "\n".join([
                "@{}".format(locations[lookup_key]),
                "D=M",

                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ])
    elif action == "pop":
        if segment in ["argument", "local", "this", "that"]:
            return "\n".join([
                "@{}".format(stack_addr),
                "D=M-1",
                "A=D",
                "D=M",
                "@temp",
                "M=D",

                "@{}".format(locations[segment]),
                "D=M",
                "@{}".format(value),
                "D=D+A",
                "@temp2",
                "M=D",

                "@temp",
                "D=M",
                "@temp2",
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M-1"
            ])
        elif segment in ["static"]: 
            return "\n".join([
                "@{}".format(stack_addr),
                "D=M-1",
                "A=D",
                "D=M", 
                "@{}.{}".format(prog_name, value),
                "M=D",
                "@{}".format(stack_addr),
                "M=M-1"
            ])
        elif segment in ["temp"]:
            return "\n".join([
                "@{}".format(stack_addr),
                "D=M-1",
                "A=D",
                "D=M",
                "@temp",
                "M=D",

                "@5",
                "D=A",
                "@{}".format(value),
                "D=D+A",
                "@temp2",
                "M=D",

                "@temp",
                "D=M",
                "@temp2",
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M-1"
            ])
        elif segment in ["pointer"]: 
            lookup_key = "this" if value == "0" else "that"
            return "\n".join([
                "@{}".format(stack_addr),
                "D=M-1",
                "A=D",
                "D=M", 
                "@{}".format(locations[lookup_key]),
                "M=D",
                "@{}".format(stack_addr),
                "M=M-1"
            ])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("You need to supply a vm file and target")
    file_name = sys.argv[1]
    target_name = sys.argv[2]
    instructions = read_instructions(file_name)
    prog_name = file_name.split("/").pop().split(".")[0]
    output = translate(prog_name, instructions)
    with open(target_name, "w") as f:
        f.write(output)

