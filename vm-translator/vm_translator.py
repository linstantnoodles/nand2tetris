import sys
import os

op_jump_index = {
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
    format_as_instruction = lambda x: "\n".join(x)
    res = [
        "@256",
        "D=A",
        "@SP",
        "M=D"
    ] + parse_function_command(["call", "Sys.init", 0])
    x = format_as_instruction(res) + "\n"
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
    if instruction[0] == "call":
        fn_name = instruction[1]
        fn_return_idx = return_index(fn_name)
        arg_count = instruction[2]
        return [
            # push return address
            "@{}$ret.{}".format(fn_name, fn_return_idx),
            "D=A", 
            "@SP", 
            "A=M",
            "M=D",
            "@SP", 
            "M=M+1",
            # push lcl into stack
            "@LCL", 
            "D=M",
            "@SP", 
            "A=M",
            "M=D",
            "@SP", 
            "M=M+1",
            # push arg into stack
            "@ARG", 
            "D=M",
            "@SP", 
            "A=M",
            "M=D",
            "@SP", 
            "M=M+1",
            # push this into stack
            "@THIS", 
            "D=M",
            "@SP", 
            "A=M",
            "M=D",
            "@SP", 
            "M=M+1",
            # push that into stack
            "@THAT", 
            "D=M",
            "@SP", 
            "A=M",
            "M=D",
            "@SP", 
            "M=M+1",
            # compute (SP - 5 - nargs) so we can reposition our argument pointer
            "@5",
            "D=A",
            "@SP",
            "D=M-D",
            "@{}".format(arg_count),
            "D=D-A",
            # reposition arg which sets the pointer to the first argument we pushed for this function call
            "@ARG",
            "M=D",
            # LCL = SP. Basically, our local segment starts right after the call frame we created (through pushing)
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
            # jump to our function and let the magic happen
            "@{}".format(fn_name),
            "0;JMP",
            # set return label. This is where we want the function to continue from
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
            # endFrame = LCL. We know this because we set our current LCL to be right after our frame.
            "@LCL",
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
            "@SP",
            "D=M-1",
            "A=D",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            "@SP",
            "M=M-1",
            # update SP. This actually reclaims the memory.
            "@ARG",
            "D=M",
            "@SP",
            "M=D+1",
            # restore THAT
            "@1",
            "D=A",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@THAT",
            "M=D",
            # restore THIS
            "@2",
            "D=A",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@THIS",
            "M=D",
            # restore ARG 
            "@3",
            "D=A",
            "A=M",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@ARG",
            "M=D",
            # restore LCL 
            "@4",
            "D=A",
            "@endFrame",
            "D=M-D",
            "A=D",
            "D=M",
            "@LCL",
            "M=D",
            # return!
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
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@{}".format(vm_instruction[1]),
            "D;JNE"
        ]

def parse_compute_command(vm_instruction):
    if vm_instruction[0] == "add":
        return [
            "@SP",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=M+D",
            "@SP",
            "M=M-1",
            "@temp",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif vm_instruction[0] == "sub":
        return [
            "@SP",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "@SP",
            "M=M-1",
            "@temp",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif vm_instruction[0] == "neg":
        return [
            "@SP",
            "A=M-1",
            "D=-M",
            "M=D"
        ]
    elif vm_instruction[0] == "eq":
        op_jump_index["eq"] += 1
        idx = op_jump_index["eq"];
        return [
            "@SP",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@SP",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "D=M",

            "@SP",
            "M=M-1",


            "@TEMP_EQUAL.{}".format(idx),
            "D;JEQ",
            "@TEMP_NOTEQUAL.{}".format(idx),
            "D;JNE",

            "(TEMP_EQUAL.{})".format(idx),
            "@SP",
            "A=M",
            "M=-1",
            "@CONTINUE_EQUAL.{}".format(idx),
            "0;JMP",

            "(TEMP_NOTEQUAL.{})".format(idx),
            "@SP",
            "A=M",
            "M=0",
            "@CONTINUE_EQUAL.{}".format(idx),
            "0;JMP",

            "(CONTINUE_EQUAL.{})".format(idx),
            "@SP",
            "M=M+1",
        ]
    elif vm_instruction[0] == "gt": 
        op_jump_index["gt"] += 1
        idx = op_jump_index["gt"];
        return [
            "@SP",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@SP",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "D=M",

            "@SP",
            "M=M-1",


            "@TEMP_GT.{}".format(idx),
            "D;JGT",
            "@TEMP_NGT.{}".format(idx),
            "D;JLE",

            "(TEMP_GT.{})".format(idx),
            "@SP",
            "A=M",
            "M=-1",
            "@CONTINUE_GT.{}".format(idx),
            "0;JMP",

            "(TEMP_NGT.{})".format(idx),
            "@SP",
            "A=M",
            "M=0",
            "@CONTINUE_GT.{}".format(idx),
            "0;JMP",

            "(CONTINUE_GT.{})".format(idx),
            "@SP",
            "M=M+1",
        ]
    elif vm_instruction[0] == "lt": 
        op_jump_index["lt"] += 1
        idx = op_jump_index["lt"];
        return [
            "@SP",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@SP",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D-M",
            "D=M",

            "@SP",
            "M=M-1",


            "@TEMP_LT.{}".format(idx),
            "D;JLT",
            "@TEMP_NLT.{}".format(idx),
            "D;JGE",

            "(TEMP_LT.{})".format(idx),
            "@SP",
            "A=M",
            "M=-1",
            "@CONTINUE_LT.{}".format(idx),
            "0;JMP",

            "(TEMP_NLT.{})".format(idx),
            "@SP",
            "A=M",
            "M=0",
            "@CONTINUE_LT.{}".format(idx),
            "0;JMP",

            "(CONTINUE_LT.{})".format(idx),
            "@SP",
            "M=M+1",
        ]
    elif vm_instruction[0] == "and":
        return [
            "@SP",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@SP",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D&M",
            "@SP",
            "M=M-1",
            "@temp",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif vm_instruction[0] == "or":
        return [
            "@SP",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",

            "@SP",
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp",
            "M=D|M",
            "@SP",
            "M=M-1",
            "@temp",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    elif vm_instruction[0] == "not":
        return [
            "@SP",
            "A=M-1",
            "D=!M",
            "M=D"
        ]

# TODO improve? talk about the jump commands in notes
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
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
        elif segment == "static":
            return [
                "@{}.{}".format(prog_name, value),
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
        elif segment in ["argument", "local", "this", "that"]:
            return [
                "@{}".format(locations[segment]),
                "D=M",
                "@{}".format(value),
                "A=D+A",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
        elif segment in ["temp"]:
            return [
                "@5",
                "D=A",
                "@{}".format(value),
                "A=D+A",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
        elif segment in ["pointer"]:
            lookup_key = "this" if value == "0" else "that"
            return [
                "@{}".format(locations[lookup_key]),
                "D=M",

                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
    elif action == "pop":
        if segment in ["argument", "local", "this", "that"]:
            return [
                "@SP",
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
                "@SP",
                "M=M-1"
            ]
        elif segment in ["static"]: 
            return [
                "@SP",
                "D=M-1",
                "A=D",
                "D=M", 
                "@{}.{}".format(prog_name, value),
                "M=D",
                "@SP",
                "M=M-1"
            ]
        elif segment in ["temp"]:
            return [
                "@SP",
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
                "@SP",
                "M=M-1"
            ]
        elif segment in ["pointer"]: 
            lookup_key = "this" if value == "0" else "that"
            return [
                "@SP",
                "D=M-1",
                "A=D",
                "D=M", 
                "@{}".format(locations[lookup_key]),
                "M=D",
                "@SP",
                "M=M-1"
            ]

def translate_file(program_name, file_name):
    if file_name[-3:] != ".vm":
        raise Exception("Invalid VM file. Missing .vm extension")
    instructions = read_instructions(file_name)
    return translate(program_name, instructions)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("You need to supply a vm file or directory")
    source = sys.argv[1]
    program_name = source.split("/").pop().split(".")[0]
    target_file_name = "{}.asm".format(program_name)
    output = ""
    if os.path.isdir(source):
        output = bootstrap()
        for file_name in read_files(source):
            output += translate_file(program_name, file_name)
    else:
        output = translate_file(program_name, source)
    with open(target_file_name, "w") as f:
        f.write(output)

