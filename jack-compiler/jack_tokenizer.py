import re 
import sys
from enum import Enum

class Token(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONSTANT = 3
    STRING_CONSTANT = 4

class Tokenizer:
    def __init__(self, source_text):
        self.source_text = source_text
        self.current_token = None 
        self.current_type = None

    def advance(self):
        while self.match_whitespace():
            self.source_text = self.source_text.lstrip()
        while self.match_comment():
            comment_match = self.match_comment()
            size = comment_match.end() - comment_match.start()
            self.source_text = self.source_text[size:]
            while self.match_whitespace():
                self.source_text = self.source_text.lstrip()
        match, token_type = self.matches_token()
        if match:
            size = match.end() - match.start()
            value = self.source_text[0:size]
            self.current_token = value
            self.current_type = token_type
            self.source_text = self.source_text[size:]
            return self.current_token

    def peek(self):
        original_token = self.current_token
        original_source_text = self.source_text
        original_type = self.current_type
        next_token = None
        next_type = None
        self.advance()
        next_token = self.current_token
        next_type = self.current_type
        self.source_text = original_source_text
        self.current_token = original_token
        self.current_type = original_type
        return next_token, next_type

    def matches_token(self):
        match = self.match_keyword()
        if match:
            return match, Token.KEYWORD
        match = self.match_identifier()
        if match:
            return match, Token.IDENTIFIER
        match = self.match_integer()
        if match:
            return match, Token.INT_CONSTANT
        match = self.match_symbol()
        if match:
            return match, Token.SYMBOL
        match = self.match_string()
        if match:
            return match, Token.STRING_CONSTANT
        return None, None

    def match_comment(self):
        res = self.match_inline_comment()
        if not res:
            return self.match_block_comment()
        return res

    def match_inline_comment(self):
        p = re.compile("\/\/.+")
        return p.match(self.source_text)

    def match_block_comment(self):
        p = re.compile("\/\*(.|\n)*?\*\/")
        return p.match(self.source_text)

    def match_identifier(self):
        p = re.compile("[a-zA-Z_][a-zA-Z0-9_]*")
        return p.match(self.source_text)

    def match_string(self):
        p = re.compile("\"[^\"]+\"")
        return p.match(self.source_text)

    def match_integer(self):
        p = re.compile("\d+")
        return p.match(self.source_text)

    def match_symbol(self):
        p = re.compile("[\{\}\(\)\[\]\.\,\;\+\-\*\/\&\|\<\>\=\~]")
        return p.match(self.source_text)

    def match_keyword(self):
        end_in_space = "(class|constructor|function|method|field|static|var|int|char|boolean|void|let|do)\\b"
        other = "true|false|null|this|if|else|while|return"
        p1 = re.compile(end_in_space)
        res = p1.match(self.source_text)
        return res if res else re.compile(other).match(self.source_text)

    def match_whitespace(self):
        p = re.compile('\s+')
        return p.match(self.source_text)

    def token_type(self):
        return self.current_type

    def key_word(self):
        if self.token_type() == Token.KEYWORD:
            return self.current_token

    def symbol(self):
        if self.token_type() == Token.SYMBOL:
            return self.current_token

    def identifier(self):
        if self.token_type() == Token.IDENTIFIER:
            return self.current_token

    def int_value(self):
        if self.token_type() == Token.INT_CONSTANT:
            return int(self.current_token)

    def string_value(self):
        if self.token_type() == Token.STRING_CONSTANT:
            return self.current_token.replace("\"","")

    def token_value(self):
        if self.token_type() == Token.KEYWORD:
            return self.current_token
        if self.token_type() == Token.SYMBOL:
            return self.symbol()
        if self.token_type() == Token.IDENTIFIER:
            return self.identifier()
        if self.token_type() == Token.INT_CONSTANT:
            return self.int_value()
        if self.token_type() == Token.STRING_CONSTANT:
            return self.string_value()

    def xml(self):
        symbol_rewrite = {
            "<": "&lt;",
            ">": "&gt;",
            "\"": "&quot;",
            "&": "&amp;"
        }
        print_symbol = lambda x: symbol_rewrite[x] if x in symbol_rewrite else x
        if self.token_type() == Token.KEYWORD:
            return "<keyword> {} </keyword>".format(self.current_token)
        if self.token_type() == Token.SYMBOL:
            return "<symbol> {} </symbol>".format(print_symbol(self.symbol()))
        if self.token_type() == Token.IDENTIFIER:
            return "<identifier> {} </identifier>".format(self.identifier())
        if self.token_type() == Token.INT_CONSTANT:
            return "<integerConstant> {} </integerConstant>".format(self.int_value())
        if self.token_type() == Token.STRING_CONSTANT:
            return "<stringConstant> {} </stringConstant>".format(self.string_value())

def tokenize(filename):
    with open(filename, 'r') as f:
        print("<tokens>")
        tokenizer = Tokenizer(f.read())
        while tokenizer.advance():
            print(tokenizer.xml())
        print("</tokens>")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("You need to supply an input file")
    file_name = sys.argv[1]
    tokenize(file_name)
