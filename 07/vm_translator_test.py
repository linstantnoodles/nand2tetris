import unittest 
import vm_translator 

class TestMemoryAccess(unittest.TestCase):
    def test_push_constant(self):
        self.assertEqual(vm_translator.parse_memory_command("prog_name", ["push", "constant", "1"]), "\n".join([
            "@1",
            "D=A",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_push_argument(self):
        self.assertEqual(vm_translator.parse_memory_command("prog_name", ["push", "argument", "1"]), "\n".join([
            "@2",
            "D=M",
            "@1",
            "A=D+A",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_push_local(self):
        self.assertEqual(vm_translator.parse_memory_command("prog_name", ["push", "local", "15"]), "\n".join([
            "@1",
            "D=M",
            "@15",
            "A=D+A",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_push_this(self):
        self.assertEqual(vm_translator.parse_memory_command("prog_name", ["push", "this", "15"]), "\n".join([
            "@3",
            "D=M",
            "@15",
            "A=D+A",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_push_that(self):
        self.assertEqual(vm_translator.parse_memory_command("prog_name", ["push", "that", "15"]), "\n".join([
            "@4",
            "D=M",
            "@15",
            "A=D+A",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_push_temp(self):
        self.assertEqual(vm_translator.parse_memory_command("prog_name", ["push", "temp", "7"]), "\n".join([
            "@5",
            "D=A",
            "@7",
            "A=D+A",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_push_pointer_0_uses_this(self):
        self.assertEqual(vm_translator.parse_memory_command("stuff", ["push", "pointer", "0"]), "\n".join([
                "@3",
                "D=M",
                "@0",
                "A=M",
                "M=D",
                "@0",
                "M=M+1"
        ]))

    def test_push_pointer_1_uses_that(self):
        self.assertEqual(vm_translator.parse_memory_command("stuff", ["push", "pointer", "1"]), "\n".join([
            "@4",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_push_static(self):
        self.assertEqual(vm_translator.parse_memory_command("Prog", ["push", "static", "3"]), "\n".join([
            "@Prog.3",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_pop_argument(self):
        self.assertEqual(vm_translator.parse_memory_command("prog", ["pop", "argument", "3"]), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M",
            "@temp",
            "M=D",

            "@2",
            "D=M",
            "@3",
            "D=D+A",
            "@temp2",
            "M=D",

            "@temp",
            "D=M",
            "@temp2",
            "A=M",
            "M=D",
            "@0",
            "M=M-1"
        ]))

    def test_pop_local(self):
        self.assertEqual(vm_translator.parse_memory_command("prog", ["pop", "local", "5"]), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M",
            "@temp",
            "M=D",

            "@1", # local segment
            "D=M",
            "@5",
            "D=D+A",
            "@temp2",
            "M=D",

            "@temp",
            "D=M",
            "@temp2",
            "A=M",
            "M=D",
            "@0",
            "M=M-1"
        ]))

    def test_pop_this(self):
        self.assertEqual(vm_translator.parse_memory_command("prog", ["pop", "this", "5"]), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M",
            "@temp",
            "M=D",

            "@3", # this segment
            "D=M",
            "@5",
            "D=D+A",
            "@temp2",
            "M=D",

            "@temp",
            "D=M",
            "@temp2",
            "A=M",
            "M=D",
            "@0",
            "M=M-1"
        ]))

    def test_pop_local(self):
        self.assertEqual(vm_translator.parse_memory_command("prog", ["pop", "that", "5"]), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M",
            "@temp",
            "M=D",

            "@4", # that segment
            "D=M",
            "@5",
            "D=D+A",
            "@temp2",
            "M=D",

            "@temp",
            "D=M",
            "@temp2",
            "A=M",
            "M=D",
            "@0",
            "M=M-1"
        ]))

    def test_pop_static(self):
        self.assertEqual(vm_translator.parse_memory_command("Prog", ["pop", "static", "2"]), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M", 
            "@Prog.2",
            "M=D",
            "@0",
            "M=M-1"
        ]))
    
    def test_pop_temp(self):
        self.assertEqual(vm_translator.parse_memory_command("Prog", ["pop", "temp", "2"]), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M",
            "@temp",
            "M=D",

            "@5",
            "D=A",
            "@2",
            "D=D+A",
            "@temp2",
            "M=D",

            "@temp",
            "D=M",
            "@temp2",
            "A=M",
            "M=D",
            "@0",
            "M=M-1"
        ]))

    def test_pop_pointer_0_sets_this_address(self):
         self.assertEqual(vm_translator.parse_memory_command("Prog", ["pop", "pointer", "0"]),"\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M", 
            "@3", # this addr
            "M=D",
            "@0",
            "M=M-1"
        ]))

    def test_pop_pointer_1_sets_that_address(self):
        self.assertEqual(vm_translator.parse_memory_command("Prog", ["pop", "pointer", "1"]),"\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M", 
            "@4", # that addr
            "M=D",
            "@0",
            "M=M-1"
        ]))

class TestStackOperations(unittest.TestCase):
    def test_translate_add(self):
        self.assertEqual(vm_translator.parse_compute_command(["add"]), "\n".join([
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
            "M=M+D",
            "@0",
            "M=M-1",
            "@temp",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_translate_sub(self):
        self.assertEqual(vm_translator.parse_compute_command(["sub"]), "\n".join([
            "@0", # load value at top of stack and store in temp
            "A=M-1",
            "D=M",
            "@temp",
            "M=D",
            "@0", # decrement stack and load next value 
            "M=M-1",
            "A=M-1",
            "D=M",
            "@temp", # store result of compute into temp
            "M=D-M",
            "@0", 
            "M=M-1",

            "@temp", # push result onto stack
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_translate_neg(self):
        self.assertEqual(vm_translator.parse_compute_command(["neg"]), "\n".join([
            "@0",
            "A=M-1",
            "D=-M",
            "M=D"
        ]))

    def test_translate_eq(self):
        self.assertEqual(vm_translator.parse_compute_command(["eq"]), "\n".join([
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

            "@TEMP_EQUAL.1",
            "D;JEQ",
            "@TEMP_NOTEQUAL.1",
            "D;JNE",

            "(TEMP_EQUAL.1)",
            "@0",
            "A=M",
            "M=-1",
            "@CONTINUE_EQUAL.1",
            "0;JMP",

            "(TEMP_NOTEQUAL.1)",
            "@0",
            "A=M",
            "M=0",
            "@CONTINUE_EQUAL.1",
            "0;JMP",

            "(CONTINUE_EQUAL.1)",
            "@0",
            "M=M+1",
        ]))

    def test_translate_lt(self):
        self.assertEqual(vm_translator.parse_compute_command(["lt"]), "\n".join([
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


            "@TEMP_LT.1",
            "D;JLT",
            "@TEMP_NLT.1",
            "D;JGE",

            "(TEMP_LT.1)",
            "@0",
            "A=M",
            "M=-1",
            "@CONTINUE_LT.1",
            "0;JMP",

            "(TEMP_NLT.1)",
            "@0",
            "A=M",
            "M=0",
            "@CONTINUE_LT.1",
            "0;JMP",

            "(CONTINUE_LT.1)",
            "@0",
            "M=M+1",
        ]))

    def test_translate_gt(self):
        self.assertEqual(vm_translator.parse_compute_command(["gt"]), "\n".join([
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


            "@TEMP_GT.1",
            "D;JGT",
            "@TEMP_NGT.1",
            "D;JLE",

            "(TEMP_GT.1)",
            "@0",
            "A=M",
            "M=-1",
            "@CONTINUE_GT.1",
            "0;JMP",

            "(TEMP_NGT.1)",
            "@0",
            "A=M",
            "M=0",
            "@CONTINUE_GT.1",
            "0;JMP",

            "(CONTINUE_GT.1)",
            "@0",
            "M=M+1"]))

    def test_translate_and(self):
        self.assertEqual(vm_translator.parse_compute_command(["and"]), "\n".join([
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
            "M=D&M",
            "@0",
            "M=M-1",
            "@temp",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_translate_or(self):
        self.assertEqual(vm_translator.parse_compute_command(["or"]), "\n".join([
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
            "M=D|M",
            "@0",
            "M=M-1",
            "@temp",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_translate_not(self):
        self.assertEqual(vm_translator.parse_compute_command(["not"]), "\n".join([
            "@0",
            "A=M-1",
            "D=!M",
            "M=D"
        ]))

if __name__ == '__main__':
    unittest.main()
