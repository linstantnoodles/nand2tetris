import unittest 
import vm_translator 

class VMTranslatorTest(unittest.TestCase):
    def test_translate(self):
        pass

    def test_pop(self):
        cmd = "pop argument 7"
        self.assertEqual(vm_translator.parse(cmd), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M",
            "@temp",
            "M=D",

            "@2",
            "D=M",
            "@7",
            "D=D+A",
            "@temp2",
            "M=D",

            "@temp",
            "D=M",
            "@temp2",
            "A=M",
            "M=D",
            "@0",
            "M=M-1",
        ]))

        cmd = "pop temp 1"
        self.assertEqual(vm_translator.parse(cmd), "\n".join([
            "@0",
            "D=M-1",
            "A=D",
            "D=M",
            "@temp",
            "M=D",

            "@5",
            "D=A",
            "@1",
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


    def test_translate_push(self):
        cmd = "push constant 7"
        self.assertEqual(vm_translator.parse(cmd), "\n".join([
            "@7",
            "D=A",
            "@0",
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_translate_push_memory(self):
        cmd = "push argument 1"
        self.assertEqual(vm_translator.parse(cmd), "\n".join([
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

    def test_translate_push_temp(self):
        cmd = "push temp 1"
        self.assertEqual(vm_translator.parse(cmd), "\n".join([
            "@5", # always base 5
            "D=A",
            "@1", # now lets get offset addr
            "A=D+A",
            "D=M",
            "@0", # update stack
            "A=M",
            "M=D",
            "@0",
            "M=M+1"
        ]))

    def test_translate_add(self):
        cmd = "add"
        self.assertEqual(vm_translator.parse(cmd), "\n".join([
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
        cmd = "sub"
        self.assertEqual(vm_translator.parse(cmd), "\n".join([
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


if __name__ == '__main__':
    unittest.main()
