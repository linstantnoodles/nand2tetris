import unittest 
import hack_assembler

class MyTest(unittest.TestCase):
    def test_decimal_to_binary(self):
        self.assertEqual(hack_assembler.decimal_to_binary(0, count=16), "0000000000000000")
        self.assertEqual(hack_assembler.decimal_to_binary(1, count=16), "0000000000000001")
        self.assertEqual(hack_assembler.decimal_to_binary(7, count=16), "0000000000000111")
        self.assertEqual(hack_assembler.decimal_to_binary(8, count=16), "0000000000001000")

    def test_instruction_lines_with_symbol_table(self):
        lines = [
            "@12",
            "D=A",
            "@0", 
            "M=D", 
            "(LABEL)", 
            "@1", 
            "M=M+1",
            "(LABEL2)",
            "@5",
            "(LABEL3)",
            "0;JMP"
        ]
        self.assertEqual(hack_assembler.instruction_lines_with_symbol_table(lines)[1]
            {
                "LABEL": hack_assembler.decimal_to_binary(4),
                "LABEL2": hack_assembler.decimal_to_binary(6),
                "LABEL3": hack_assembler.decimal_to_binary(7)
            }
        )

if __name__ == "__main__":
    unittest.main()
