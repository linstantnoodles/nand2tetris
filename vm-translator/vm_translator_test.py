import unittest 
import vm_translator 

class TestTranslation(unittest.TestCase):
    def test_translation(self):
        lines = ["push constant 1", "push constant 2"]
        result = vm_translator.translate("Prog", lines)
        expected_first_line = "\n".join([
            "@1",
            "D=A",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ])
        expected_second_line = "\n".join([
            "@2",
            "D=A",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ])
        self.assertEqual("\n".join([expected_first_line, expected_second_line]) + "\n", result)

    def test_is_instruction(self):
        self.assertFalse(vm_translator.is_instruction("// wowthere"))
        self.assertTrue(vm_translator.is_instruction("push constant 1 // testing"))

class TestMemoryAccess(unittest.TestCase):
    def test_push_constant(self):
        result = vm_translator.parse_memory_command("prog_name", ["push", "constant", "1"])
        self.assertEqual(result, [
            "@1",
            "D=A",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ])

    def test_push_argument(self):
        result = vm_translator.parse_memory_command("prog_name", ["push", "argument", "1"])
        self.assertEqual(result, [
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
        ])

    def test_push_local(self):
        result = vm_translator.parse_memory_command("prog_name", ["push", "local", "15"]) 
        self.assertEqual(result, [
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
        ])

    def test_push_this(self):
        result = vm_translator.parse_memory_command("prog_name", ["push", "this", "15"])
        self.assertEqual(result, [
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
        ])

    def test_push_that(self):
        result = vm_translator.parse_memory_command("prog_name", ["push", "that", "15"])
        self.assertEqual(result, [
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
        ])

    def test_push_temp(self):
        result = vm_translator.parse_memory_command("prog_name", ["push", "temp", "7"])
        self.assertEqual(result, [
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
        ])

    def test_push_pointer_0_uses_this(self):
        result = vm_translator.parse_memory_command("stuff", ["push", "pointer", "0"])
        self.assertEqual(result, [
                "@3",
                "D=M",
                "@0",
                "A=M",
                "M=D",
                "@0",
                "M=M+1"
        ])

    def test_push_pointer_1_uses_that(self):
        result = vm_translator.parse_memory_command("stuff", ["push", "pointer", "1"])
        self.assertEqual(result, [
            "@4",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ])

    def test_push_static(self):
        result = vm_translator.parse_memory_command("Prog", ["push", "static", "3"])
        self.assertEqual(result, [
            "@Prog.3",
            "D=M",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ])

    def test_pop_argument(self):
        result = vm_translator.parse_memory_command("prog", ["pop", "argument", "3"])
        self.assertEqual(result, [
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
        ])

    def test_pop_local(self):
        result = vm_translator.parse_memory_command("prog", ["pop", "local", "5"])
        self.assertEqual(result, [
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
        ])

    def test_pop_this(self):
        result = vm_translator.parse_memory_command("prog", ["pop", "this", "5"])
        self.assertEqual(result, [
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
        ])

    def test_pop_local(self):
        result = vm_translator.parse_memory_command("prog", ["pop", "that", "5"])
        self.assertEqual(result, [
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
        ])

    def test_pop_static(self):
        result = vm_translator.parse_memory_command("Prog", ["pop", "static", "2"])
        self.assertEqual(result, [
            "@0",
            "D=M-1",
            "A=D",
            "D=M", 
            "@Prog.2",
            "M=D",
            "@0",
            "M=M-1"
        ])
    
    def test_pop_temp(self):
        result = vm_translator.parse_memory_command("Prog", ["pop", "temp", "2"])
        self.assertEqual(result, [
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
        ])

    def test_pop_pointer_0_sets_this_address(self):
        result = vm_translator.parse_memory_command("Prog", ["pop", "pointer", "0"])
        self.assertEqual(result, [
            "@0",
            "D=M-1",
            "A=D",
            "D=M", 
            "@3", # this addr
            "M=D",
            "@0",
            "M=M-1"
        ])

    def test_pop_pointer_1_sets_that_address(self):
        result = vm_translator.parse_memory_command("Prog", ["pop", "pointer", "1"])
        self.assertEqual(result, [
            "@0",
            "D=M-1",
            "A=D",
            "D=M", 
            "@4", # that addr
            "M=D",
            "@0",
            "M=M-1"
        ])

class TestStackOperations(unittest.TestCase):
    def test_translate_add(self):
        result = vm_translator.parse_compute_command(["add"])
        self.assertEqual(result, [
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
        ])

    def test_translate_sub(self):
        result = vm_translator.parse_compute_command(["sub"])
        self.assertEqual(result, [
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
        ])

    def test_translate_neg(self):
        result = vm_translator.parse_compute_command(["neg"])
        self.assertEqual(result, [
            "@0",
            "A=M-1",
            "D=-M",
            "M=D"
        ])

    def test_translate_eq(self):
        result = vm_translator.parse_compute_command(["eq"])
        self.assertEqual(result, [
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
        ])

    def test_translate_lt(self):
        result = vm_translator.parse_compute_command(["lt"])
        self.assertEqual(result, [
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
        ])

    def test_translate_gt(self):
        result_one = vm_translator.parse_compute_command(["gt"])
        result_two = vm_translator.parse_compute_command(["gt"])
        self.assertEqual(result_one, [
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
            "M=M+1"])
        self.assertEqual(result_two, [
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


            "@TEMP_GT.2",
            "D;JGT",
            "@TEMP_NGT.2",
            "D;JLE",

            "(TEMP_GT.2)",
            "@0",
            "A=M",
            "M=-1",
            "@CONTINUE_GT.2",
            "0;JMP",

            "(TEMP_NGT.2)",
            "@0",
            "A=M",
            "M=0",
            "@CONTINUE_GT.2",
            "0;JMP",

            "(CONTINUE_GT.2)",
            "@0",
            "M=M+1"])

    def test_translate_and(self):
        result = vm_translator.parse_compute_command(["and"])
        self.assertEqual(result, [
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
        ])

    def test_translate_or(self):
        result = vm_translator.parse_compute_command(["or"])
        self.assertEqual(result, [
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
        ])

    def test_translate_not(self):
        result = vm_translator.parse_compute_command(["not"])
        self.assertEqual(result, [
            "@0",
            "A=M-1",
            "D=!M",
            "M=D"
        ])

class TestConditionals(unittest.TestCase):
    def test_translate_label(self):
        result = vm_translator.parse_branch_command(["label", "LOOPSTART"])
        self.assertEqual(result, ["(LOOPSTART)"])

    def test_translate_unconditonal_jump(self):
        result = vm_translator.parse_branch_command(["goto", "LOOPSTART"])
        self.assertEqual(result, [
            "@LOOPSTART",
            "0;JMP"
        ])

    def test_translate_conditional_jump(self):
        result = vm_translator.parse_branch_command(["if-goto", "LOOPSTART"])
        self.assertEqual(result, [
            "@0",
            "M=M-1",
            "A=M",
            "D=M",
            "@LOOPSTART",
            "D;JNE"
        ])

class TestFunctionCalls(unittest.TestCase):
    def xtest_translate_call_function(self):
        result = vm_translator.parse_function_command(["call", "foobar", "3"])
        self.assertEqual(result, [""])

    def xtest_translate_function_def(self):
        result = vm_translator.parse_function_command(["function", "foobar", "3"])
        self.assertEqual(result, ["(foobar)"])

    def test_translate_function_return(self):
        result = vm_translator.parse_function_command(["return"])
        self.assertEqual(result, [])

    def test_function_calls_update_return_index(self):
        result = vm_translator.parse_function_command(["call", "foobar", "1"])
        self.assertIn("@foobar$ret.1", result)
        next_result = vm_translator.parse_function_command(["call", "foobar", "1"])
        self.assertIn("@foobar$ret.2", next_result)

if __name__ == '__main__':
    unittest.main()
