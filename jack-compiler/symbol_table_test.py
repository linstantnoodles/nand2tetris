import unittest 
from symbol_table import SymbolTable 

class TestSymbolTable(unittest.TestCase):
    def test_defining_var_count(self):
        table = SymbolTable()
        table.define("x", "int", "var")
        table.define("y", "int", "var")
        table.define("z", "int", "field")
        table.define("k", "int", "static")
        table.define("j", "int", "arg")
        self.assertEqual(table.var_count("var"), 2)
        self.assertEqual(table.var_count("field"), 1)
        self.assertEqual(table.var_count("static"), 1)
        self.assertEqual(table.var_count("arg"), 1)

    def test_defining_var_with_index_running(self):
        table = SymbolTable()
        table.define("x", "int", "var")
        table.define("y", "int", "var")
        self.assertEqual(table.index_of("x"), 0)
        self.assertEqual(table.index_of("y"), 1)

    def test_defining_var_with_scopes(self):
        table = SymbolTable()
        table.define("x", "int", "var")
        table.define("x", "int", "field")

        self.assertEqual(table.index_of("x"), 0)
        self.assertEqual(table.kind_of("x"), "var")

    def test_kind_of_when_var_exists(self):
        table = SymbolTable()
        table.define("j", "int", "arg")
        self.assertEqual(table.kind_of("j"), "arg")

    def test_kind_of_when_var_missing(self):
        table = SymbolTable()
        self.assertIsNone(table.kind_of("nonexistent"))

    def test_type_of(self):
        table = SymbolTable()
        table.define("j", "int", "arg")
        self.assertEqual(table.type_of("j"), "int")

    def test_type_of_with_scope(self):
        table = SymbolTable()
        table.define("j", "int", "arg")
        table.define("j", "bool", "field")
        self.assertEqual(table.type_of("j"), "int")

    def test_start_subroutine(self):
        table = SymbolTable()
        table.define("x", "int", "var")
        table.define("y", "int", "var")
        table.define("y", "int", "field")

        table.start_subroutine()

        self.assertEqual(table.var_count("var"), 0)
        self.assertEqual(table.var_count("field"), 1)

if __name__ == "__main__":
    unittest.main()
