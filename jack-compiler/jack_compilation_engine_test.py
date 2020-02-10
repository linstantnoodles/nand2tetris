import unittest 
from jack_compilation_engine import JackCompilationEngine 

class TestJackCompilationEngine(unittest.TestCase):
    def test_eat_keyword_when_does_not_exist(self):
        engine = JackCompilationEngine("lass Test { }")
        with self.assertRaises(RuntimeError):
            engine.eat_keyword('class')

if __name__ == "__main__":
    unittest.main()
