import sys
import os

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
function_return_index = {}

def return_index(name):
    if name in function_return_index:
        function_return_index[name] += 1
    else:
        function_return_index[name] = 1
    return function_return_index[name]

def bootstrap():
    print("--bootstrap--")
    format_as_instruction = lambda x: "\n".join(x)
    res = [
        "@261",
        "D=A",
        "@0",
        "M=D",
        "@Sys.init",
        "0;JMP"
        ] 
    x = format_as_instruction(res) + "\n"
    print(x)
    return x

def read_files(folder_path):
    file_list = os.listdir(folder_path)
    files = [os.path.join(folder_path, file_name) for file_name in file_list if ".vm" in file_name]
    return files

def read_instructions(filename):
    with open(filename, 'r') as f:
       contents = f.read()
       return [x.strip() for x in contents.split('\n') if is_instruction(x)]

def is_instruction(line):
    return line.strip() and line[0:2] != "//"

def translate(prog_name, instructions):
    parsed = [parse(prog_name, instruction) for instruction in instructions]
    return "\n".join(parsed) + "\n"

def parse(prog_name, vm_instruction):
    chunked = [x.strip() for x in vm_instruction.split(" ")]
    print("--{}--".format(chunked))
    format_as_instruction = lambda x: "\n".join(x)
    res = None
    if is_branching_command(chunked):
        res = format_as_instruction(parse_branch_command(chunked))
    if is_function_command(chunked):
        res = format_as_instruction(parse_function_command(chunked))
    if is_memory_command(chunked):
        res = format_as_instruction(parse_memory_command(prog_name, chunked))
    if is_compute_command(chunked):
        res = format_as_instruction(parse_compute_command(chunked))
    print(res)
    return res
def is_branching_command(instruction):
    return instruction[0] in ["label", "goto", "if-goto"]

def is_memory_command(instruction):
    return instruction[0] in ["push", "pop"]

def is_compute_command(instruction):
    return instruction[0] in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

def is_function_command(instruction):
    return instruction[0] in ["call", "function", "return"]

def parse_function_command(instruction):
    # every call has a corresponding return for this function
    if instruction[0] == "call":
        fn_name = instruction[1]
        fn_return_idx = return_index(fn_name)
        arg_count = instruction[2]
        return [
            # push return address
            "@{}$ret.{}".format(fn_name, fn_return_idx),
            "D=A", 
            "@{}".format(stack_addr), 
            "A=M",
            "M=D",
            # increment pointer
            "@{}".format(stack_addr), 
            "M=M+1",

            # push lcl into stack
            "@{}".format(local_addr), 
            "D=M",
            "@{}".format(stack_addr), 
            "A=M",
            "M=D",
            "@{}".format(stack_addr), 
            "M=M+1",

            # push arg into stack
            "@{}".format(arg_addr), 
            "D=M",
            "@{}".format(stack_addr), 
            "A=M",
            "M=D",
            "@{}".format(stack_addr), 
            "M=M+1",

            # push this into stack
            "@{}".format(this_addr), 
            "D=M",
            "@{}".format(stack_addr), 
            "A=M",
            "M=D",
            "@{}".format(stack_addr), 
            "M=M+1",

            # push that into stack
            "@{}".format(that_addr), 
            "D=M",
            "@{}".format(stack_addr), 
            "A=M",
            "M=D",
            "@{}".format(stack_addr), 
            "M=M+1",

            # SP - 5 - nargs
            "@5",
            "D=A",
            "@{}".format(stack_addr),
            "D=M-D",
            "@{}".format(arg_count),
            "D=D-A",

            # reposition arg
            "@{}".format(arg_addr),
            "M=D",

            # LCL = SP
            "@0",
            "D=M",
            "@{}".format(local_addr),
            "M=D",

            # jump
            "@{}".format(fn_name),
            "0;JMP",

            # set return label 
            "({}$ret.{})".format(fn_name, fn_return_idx)
        ]
    if instruction[0] == "function":
        nVars = int(instruction[2])
        push_cmds = []
        for i in range(nVars):
            push_cmds += parse_memory_command(i, ["push", "constant", "0"])
        return ["({})".format(instruction[1])] + push_cmds
    if instruction[0] == "return":
        return [
            # endFrame = LCL
            "@{}".format(local_addr),
            "D=M",
            "@endFrame",
            "M=D",
            # returnAddr = endFrame - 5. Save for later. Since we'll be adding back LCL
            "@5",
            "D=D-A",
            "A=D",
            "D=M",
            "@returnAddr",
            "M=D",

            # Set *ARG=result (value at top of stack)
            "@{}".format(stack_addr),
            "D=M-1",
            "A=D",
            "D=M",
            "@{}".format(arg_addr),
            "A=M",
            "M=D",
            "@{}".format(stack_addr),
            "M=M-1",

            # update SP
            "@{}".format(arg_addr),
            "D=M",
            "@{}".format(stack_addr),
            "M=D+1",

            # set LCL
            "@1",
            "D=A",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@{}".format(that_addr),
            "M=D",

            # set ARG
            "@2",
            "D=A",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@{}".format(this_addr),
            "M=D",

            # set THIS
            "@3",
            "D=A",
            "A=M",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@{}".format(arg_addr),
            "M=D",

            # set THAT
            "@4",
            "D=A",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@{}".format(local_addr),
            "M=D",

            # return
            "@returnAddr",
            "A=M",
            "0;JMP"
        ]

def parse_branch_command(vm_instruction):
    if vm_instruction[0] == "label": 
        return [
            "({})".format(vm_instruction[1])
        ]
    if vm_instruction[0] == "goto":
        return [
            "@{}".format(vm_instruction[1]),
            "0;JMP"
        ]
    if vm_instruction[0] == "if-goto": 
        return [
            "@{}".format(stack_addr),
            "M=M-1",
            "A=M",
            "D=M",
            "@{}".format(vm_instruction[1]),
            "D;JNE"
        ]

def parse_compute_command(vm_instruction):
    if vm_instruction[0] == "add":
        return [
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
        ]
    elif vm_instruction[0] == "sub":
        return [
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
        ]
    elif vm_instruction[0] == "neg":
        return [
            "@{}".format(stack_addr),
            "A=M-1",
            "D=-M",
            "M=D"
        ]
    elif vm_instruction[0] == "eq":
        inequality_counter["eq"] += 1
        idx = inequality_counter["eq"];
        return [
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
        ]
    elif vm_instruction[0] == "gt": 
        inequality_counter["gt"] += 1
        idx = inequality_counter["gt"];
        return [
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
        ]
    elif vm_instruction[0] == "lt": 
        inequality_counter["lt"] += 1
        idx = inequality_counter["lt"];
        return [
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
        ]
    elif vm_instruction[0] == "and":
        return [
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
        ]
    elif vm_instruction[0] == "or":
        return [
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
        ]
    elif vm_instruction[0] == "not":
        return [
            "@{}".format(stack_addr),
            "A=M-1",
            "D=!M",
            "M=D"
        ]

def parse_memory_command(prog_name, vm_instruction):
    action, segment, value = vm_instruction[0], vm_instruction[1], vm_instruction[2]
    locations = {
        "local": 1,
        "argument": 2,
        "this": 3,
        "that": 4
    }
    if action == "push":
        if segment == "constant":
            return [
                "@{}".format(value),
                "D=A",
                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ]
        elif segment == "static":
            return [
                "@{}.{}".format(prog_name, value),
                "D=M",
                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ]
        elif segment in ["argument", "local", "this", "that"]:
            return [
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
            ]
        elif segment in ["temp"]:
            return [
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
            ]
        elif segment in ["pointer"]:
            lookup_key = "this" if value == "0" else "that"
            return [
                "@{}".format(locations[lookup_key]),
                "D=M",

                "@{}".format(stack_addr),
                "A=M",
                "M=D",
                "@{}".format(stack_addr),
                "M=M+1"
            ]
    elif action == "pop":
        if segment in ["argument", "local", "this", "that"]:
            return [
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
            ]
        elif segment in ["static"]: 
            return [
                "@{}".format(stack_addr),
                "D=M-1",
                "A=D",
                "D=M", 
                "@{}.{}".format(prog_name, value),
                "M=D",
                "@{}".format(stack_addr),
                "M=M-1"
            ]
        elif segment in ["temp"]:
            return [
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
            ]
        elif segment in ["pointer"]: 
            lookup_key = "this" if value == "0" else "that"
            return [
                "@{}".format(stack_addr),
                "D=M-1",
                "A=D",
                "D=M", 
                "@{}".format(locations[lookup_key]),
                "M=D",
                "@{}".format(stack_addr),
                "M=M-1"
            ]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("You need to supply a vm file and target")
    file_name = sys.argv[1]
    target_name = sys.argv[2]
    if os.path.isdir(file_name):
        files = read_files(file_name)
        output = bootstrap()
        for file_name in files:
            instructions = read_instructions(file_name)
            prog_name = file_name.split("/").pop().split(".")[0]
            output += translate(prog_name, instructions)
        with open(target_name, "w") as f:
            f.write(output)
    else:
        instructions = read_instructions(file_name)
        prog_name = file_name.split("/").pop().split(".")[0]
        output = translate(prog_name, instructions)
        with open(target_name, "w") as f:
            f.write(output)

