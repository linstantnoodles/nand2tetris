import unittest 
from jack_tokenizer import Tokenizer, Token

class TestTokenizer(unittest.TestCase):
    def test_match_whitespace(self):
        t = Tokenizer("   ")
        self.assertIsNotNone(t.match_whitespace())
        t = Tokenizer("")
        self.assertIsNone(t.match_whitespace())

    def test_match_comment(self):
        t = Tokenizer("//wow\n")
        self.assertIsNotNone(t.match_comment())
        t = Tokenizer("/* wow */")
        self.assertIsNotNone(t.match_comment())
        t = Tokenizer("// and the book \"The Elements of Computing Systems\"")
        self.assertIsNotNone(t.match_comment())
        t = Tokenizer("/** wow */")
        self.assertIsNotNone(t.match_comment())
    
    def test_do_ambiguity(self):
        t = Tokenizer("do something()") 
        self.assertIsNotNone(t.match_keyword())
        t = Tokenizer("dosomething()") 
        self.assertIsNone(t.match_keyword())

    def test_match_keyword(self):
        keywords = [
            "class",
            "constructor",
            "function",
            "method",
            "field",
            "static",
            "var",
            "int",
            "char",
            "boolean",
            "void",
            "true",
            "false",
            "null",
            "this",
            "let",
            "do",
            "if",
            "else",
            "while",
            "return"
        ]
        for keyword_value in keywords: 
            t = Tokenizer(keyword_value)
            self.assertIsNotNone(t.match_keyword())

    def test_match_symbol(self):
        symbols = [
            "{",
            "}",
            "(",
            ")",
            "[",
            "]",
            ".",
            ",",
            ";",
            "+",
            "-",
            "*",
            "/",
            "&",
            "|",
            "<",
            ">",
            "=",
            "~"
        ]
        for symbol in symbols: 
            t = Tokenizer(symbol)
            self.assertIsNotNone(t.match_symbol())

    def test_match_integer(self):
        t = Tokenizer("12324")
        self.assertIsNotNone(t.match_integer())
        t = Tokenizer("df")
        self.assertIsNone(t.match_integer())

    def test_match_string(self):
        t = Tokenizer("\"sup\"")
        self.assertIsNotNone(t.match_string())
        t = Tokenizer("\"sup")
        self.assertIsNone(t.match_string())

    def test_match_identifier(self):
        t = Tokenizer("wow_")
        self.assertIsNotNone(t.match_identifier())
        t = Tokenizer("heya_dude")
        self.assertIsNotNone(t.match_identifier())
        t = Tokenizer("5heya_dude")
        self.assertIsNone(t.match_identifier())
    
    def test_has_more_tokens(self):
        test_input = "let x = 5"
        t = Tokenizer(test_input)
        self.assertIsNotNone(t.matches_token()[0])

    def test_advance_simple(self):
        test_input = """let x = 5"""
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.source_text, " x = 5")

    def test_advance_with_whitespace(self):
        test_input = """            let x = 5"""
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.source_text, " x = 5")

    def test_advance_with_comments(self):
        test_input = "/*thisisacomment*/ let x = 5"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.source_text, " x = 5")

        test_input = """// a comment\n// another comment\nlet x = 5"""
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.source_text, " x = 5")

    def test_token_type(self):
        test_input = "let x = 5"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.token_type(), Token.KEYWORD)
    
        test_input = "-3"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.token_type(), Token.SYMBOL)

        test_input = "345 + 3"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.token_type(), Token.INT_CONSTANT)

        test_input = "\"supthere\""
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.token_type(), Token.STRING_CONSTANT)

        test_input = "x = 5"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.token_type(), Token.IDENTIFIER)

    def test_key_word(self):
        test_input = "class A"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.key_word(), "class")

        test_input = "field b"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.key_word(), "field")

    def test_symbol(self):
        test_input = "{a}"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.symbol(), "{")

    def test_identifier(self):
        test_input = "xyz = 5"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.identifier(), "xyz")

    def test_int_value(self):
        test_input = "5"
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.int_value(), 5)

    def test_string_value(self):
        test_input = "\"test\""
        t = Tokenizer(test_input)
        t.advance()
        self.assertEqual(t.string_value(), "test")

if __name__ == "__main__":
    unittest.main()
