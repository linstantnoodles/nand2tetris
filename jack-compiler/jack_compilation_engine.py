import os
import sys
from jack_tokenizer import Tokenizer, Token
from jack_vm_writer import JackVMWriter, Segment, Command
from symbol_table import SymbolTable

class JackCompilationEngine:
    def __init__(self, source_text):
        self.tokenizer = Tokenizer(source_text)
        self.code_writer = JackVMWriter()
        self.symbol_table = SymbolTable()
        self.segment_map = {
            "var": Segment.LOCAL,
            "arg": Segment.ARG,
            "static": Segment.STATIC,
            "field": Segment.THIS,
        }
        self.cond_label_index = {
            "if": 0,
            "while": 0
        }
        self.class_name = None

    """
    <class> =>
        'class' <className> '{' <classVarDec>* <subroutineDec>* '}'
    """
    def compile_class(self):
        print("<class>")
        self.eat_keyword('class')
        self.class_name = self.eat_identifier()
        self.eat_symbol('{')
        self.compile_class_var_dec()
        self.compile_subroutine_zero_or_more()
        self.eat_symbol('}')
        print("</class>")

    """
    <classVarDec> =>
      '(' ('static' | 'field') <type> <varName> (',' <varName>)* ';'
    """
    def compile_class_var_dec(self):
        lhs_values = ["static", "field"]
        next_token, _ = self.tokenizer.peek()
        while next_token in lhs_values:
            print("<classVarDec>")

            iden_kind = self.eat_keyword_or(['static', 'field'])
            iden_type = self.compile_type()
            iden_name = self.eat_identifier()
            self.symbol_table.define(iden_name, iden_type, iden_kind)

            self.compile_varname_zero_or_more(iden_type, iden_kind)
            self.eat_symbol(';')

            print("</classVarDec>")
            next_token, _ = self.tokenizer.peek()

    """
    <type> => 'int' | 'char' | 'boolean' | <className>
    """
    def compile_type(self):
        next_token, _ = self.tokenizer.peek()
        keywords = ["int", "char", "boolean"]
        if next_token in keywords:
            return self.eat_keyword_or(keywords)
        else:
            return self.eat_identifier() 

    def compile_subroutine_zero_or_more(self):
        lhs_values = ["constructor", "function", "method"]
        next_token, _ = self.tokenizer.peek()
        while next_token in lhs_values:
            self.compile_subroutine()
            next_token, _ = self.tokenizer.peek()

    """
    <subroutineDec> =>
      ('constructor' | 'function' | 'method')
      ('void' | <type>) <subroutineName> '(' <parameterList> ')'
      <subroutineBody>
    """
    def compile_subroutine(self):
        print("<subroutineDec>")
        self.symbol_table.start_subroutine()

        subroutine_kind = self.eat_keyword_or(["constructor", "function", "method"])

        if subroutine_kind == "method":
            self.symbol_table.define("this", self.class_name, "arg")

        next_token, _ = self.tokenizer.peek()

        if next_token == 'void':
            subroutine_type = self.eat_keyword('void')
        else:
            subroutine_type = self.compile_type()

                    
        subroutine_name = self.eat_identifier()
        self.eat_symbol("(")
        self.compile_parameter_list()
        self.eat_symbol(")")
        
        subroutine_name = "{}.{}".format(self.class_name, subroutine_name)
        self.compile_subroutine_body(subroutine_name, subroutine_kind)

        if subroutine_type == "void":
            self.code_writer.write_push(Segment.CONST, 0)

        self.code_writer.write_return()
        print("</subroutineDec>")

    """
    <parameterList> =>
        (<type> <varName> (',' <type> <varName>)* )?
    """
    def compile_parameter_list(self):
        print("<parameterList>")
        next_token, next_type = self.tokenizer.peek()
        type_keywords = ['int', 'char', 'boolean']
        if next_token in type_keywords or next_type == Token.IDENTIFIER: 
            self.compile_parameter()
            self.compile_parameter_zero_or_more()
        print("</parameterList>")

    def compile_parameter(self):
        param_type = self.compile_type()
        param_name = self.eat_identifier()
        self.symbol_table.define(param_name, param_type, "arg")

    def compile_parameter_zero_or_more(self):
        next_token, _ = self.tokenizer.peek()
        while next_token == ",":
            self.eat_symbol(",")
            self.compile_parameter()
            next_token, _ = self.tokenizer.peek()

    """
    <subroutineBody> => '{' <varDec>* <statements> '}'
    """
    def compile_subroutine_body(self, subroutine_name, subroutine_kind):
        print("<subroutineBody>")
        self.eat_symbol("{")
        
        self.compile_var_dec_zero_or_more()

        self.code_writer.write_function(subroutine_name, self.symbol_table.var_count("var"))

        if subroutine_kind == "method":
            self.code_writer.write_push(Segment.ARG, 0)
            self.code_writer.write_pop(Segment.POINTER, 0)
        if subroutine_kind == "constructor":
            self.code_writer.write_push(Segment.CONST, self.symbol_table.var_count("field"))
            self.code_writer.write_call("Memory.alloc", 1)
            self.code_writer.write_pop(Segment.POINTER, 0)

        self.compile_statements()
        self.eat_symbol("}")
        print("</subroutineBody>")

    def compile_var_dec_zero_or_more(self):
        next_token, _ = self.tokenizer.peek()
        while next_token == "var":
            self.compile_var_dec()
            next_token, _ = self.tokenizer.peek()

    """
    <varDec> => 'var' <type> <varName> (',' <varName>)* ';'
    """
    def compile_var_dec(self):
        print("<varDec>")
        iden_kind = self.eat_keyword("var")
        iden_type = self.compile_type()
        iden_name = self.eat_identifier()

        self.symbol_table.define(iden_name, iden_type, iden_kind)

        self.compile_varname_zero_or_more(iden_type, iden_kind)

        self.eat_symbol(";")
        print("</varDec>")

    def compile_varname_zero_or_more(self, iden_type, iden_kind):
        next_token, _ = self.tokenizer.peek()
        while next_token == ",":
            self.eat_symbol(',')
            iden_name = self.eat_identifier()

            self.symbol_table.define(iden_name, iden_type, iden_kind)

            next_token, _ = self.tokenizer.peek()

    """
    <statements> =>
      ( <letStatement> | <ifStatement> | <whileStatement> |
        <doStatement> | <returnStatement>
        <statement> )*
    """
    def compile_statements(self):
        print("<statements>")
        next_token, _ = self.tokenizer.peek()
        while next_token in ["let", "if", "while", "do", "return"]:
            if next_token == "let":
                self.compile_let_statement()
            elif next_token == "if":
                self.compile_if_statement()
            elif next_token == "while":
                self.compile_while_statement()
            elif next_token == "do":
                self.compile_do_statement()
            elif next_token == "return":
                self.compile_return_statement()
            next_token, _ = self.tokenizer.peek()
        print("</statements>")

    """
    <letStatement> => 'let' identifier ('[' <expression> ']')? '=' <expression> ';'
    """
    def compile_let_statement(self):
        print("<letStatement>")
        self.eat_keyword("let")
        iden_name = self.eat_identifier()
        iden_type = self.symbol_table.type_of(iden_name)
        iden_index = self.symbol_table.index_of(iden_name)
        iden_segment = self.segment_map[self.symbol_table.kind_of(iden_name)]

        next_token, _ = self.tokenizer.peek()
        if next_token == "[":
            self.code_writer.write_push(iden_segment, iden_index)

            self.eat_symbol('[')
            self.compile_expression()

            self.code_writer.write_arithmetic(Command.ADD)
            
            self.eat_symbol(']')

        self.eat_symbol('=')
        self.compile_expression()
        
        if next_token == "[":
            self.code_writer.write_pop(Segment.TEMP, 0)
            self.code_writer.write_pop(Segment.POINTER, 1)
            self.code_writer.write_push(Segment.TEMP, 0)
            self.code_writer.write_pop(Segment.THAT, 0) 
        else:
            self.code_writer.write_pop(iden_segment, iden_index) 

        self.eat_symbol(';')
        print("</letStatement>")

    """
    <ifStatement> =>
      'if' '(' <expression> ')' '{' statements> '}'
      ('else' '{' statements> '}')?
    """
    def compile_if_statement(self):
        print("<ifStatement>")

        self.eat_keyword("if")
        self.eat_symbol("(")
        self.compile_expression()
        self.eat_symbol(")")
        self.eat_symbol("{")

        self.code_writer.write_arithmetic(Command.NOT)

        false_label = "IF_LABEL_FALSE.{}".format(self.cond_label_index['if'])
        end_label = "IF_LABEL_END.{}".format(self.cond_label_index['if'])
        self.cond_label_index['if'] = self.cond_label_index['if'] + 1

        self.code_writer.write_if(false_label)
        self.compile_statements()
        
        self.code_writer.write_goto(end_label)

        self.eat_symbol("}")

        self.code_writer.write_label(false_label)
        next_token, next_type = self.tokenizer.peek()
        if next_type == Token.KEYWORD and next_token == "else":
            self.eat_keyword("else")
            self.eat_symbol("{")
            self.compile_statements()
            self.eat_symbol("}")

        self.code_writer.write_label(end_label)
        print("</ifStatement>")

    """
    <whileStatement> =>
      'while' '(' <expression> ')' '{' statements> '}'
      ('else' '{' statements> '}')?
    """
    def compile_while_statement(self):
        print("<whileStatement>")

        start_label = "WHILE_LABEL_START.{}".format(self.cond_label_index['while'])
        false_label = "WHILE_LABEL_ELSE.{}".format(self.cond_label_index['while'])
        self.cond_label_index['while'] = self.cond_label_index['while'] + 1

        self.code_writer.write_label(start_label)

        self.eat_keyword("while")
        self.eat_symbol("(")

        self.compile_expression()

        self.code_writer.write_arithmetic(Command.NOT)
        self.code_writer.write_if(false_label)

        self.eat_symbol(")")
        self.eat_symbol("{")
        self.compile_statements()
        self.eat_symbol("}")

        self.code_writer.write_goto(start_label)
        self.code_writer.write_label(false_label)

        next_token, next_type = self.tokenizer.peek()
        if next_type == Token.KEYWORD and next_token == "else":
            self.eat_keyword("else")
            self.eat_symbol("{")
            self.compile_statements()
            self.eat_symbol("}")

        print("</whileStatement>")

    """
    <doStatement> => 'do' <subroutineCall> ';'
    """
    def compile_do_statement(self):
        print("<doStatement>")
        self.eat_keyword("do")
        self.compile_subroutine_call()
        self.eat_symbol(";")

        self.code_writer.write_pop(Segment.TEMP, 0)
        print("</doStatement>")

    """
    <returnStatement> => 'return' <expression>? ';'
    """
    def compile_return_statement(self):
        print("<returnStatement>")
        self.eat_keyword("return")

        next_token, next_type = self.tokenizer.peek()
        if next_token != ";":
            self.compile_expression()

        self.eat_symbol(";")
        print("</returnStatement>")

    """
    <expression> =>
        <term> (<op> <term>)*
    """
    def compile_expression(self):
        print("<expression>")
        self.compile_term()
        self.compile_term_operations_zero_or_more()
        print("</expression>")

    def compile_term_operations_zero_or_more(self):
        next_token, _ = self.tokenizer.peek()
        binary_operators = ['+' , '-' , '*' , '/' , '|',  '&' , '<' , '>' , '=']
        while next_token in binary_operators:
            self.eat_symbol(next_token)
            self.compile_term()
            if next_token == "+":
                self.code_writer.write_arithmetic(Command.ADD)
            elif next_token == "*":
                self.code_writer.write_call("Math.multiply", 2)
            elif next_token == "/":
                self.code_writer.write_call("Math.divide", 2)
            elif next_token == "-":
                self.code_writer.write_arithmetic(Command.SUB)
            elif next_token == "|":
                self.code_writer.write_arithmetic(Command.OR)
            elif next_token == "&":
                self.code_writer.write_arithmetic(Command.AND)
            elif next_token == "<":
                self.code_writer.write_arithmetic(Command.LT)
            elif next_token == ">":
                self.code_writer.write_arithmetic(Command.GT)
            elif next_token == "=":
                self.code_writer.write_arithmetic(Command.EQ)
            next_token, _ = self.tokenizer.peek()

    """
    <term> =>
      integerConstant | stringConstant | keywordConstant |
     <varName> | <varName> '[' <expression> ']' | <subroutineCall> |
     '(' <expression> ')' | unaryOp <term>
    """
    def compile_term(self):
        print("<term>")
        next_token, next_type = self.tokenizer.peek()
        lhs_literal_types = [Token.INT_CONSTANT, Token.STRING_CONSTANT, Token.KEYWORD]
        if next_type in lhs_literal_types:
            if next_type == Token.INT_CONSTANT:
                value = self.eat_integer()
                self.code_writer.write_push(Segment.CONST, value)
            elif next_type == Token.STRING_CONSTANT:
                value = self.eat_string()
                str_length = len(value)
                self.code_writer.write_push(Segment.CONST, str_length)
                self.code_writer.write_call("String.new", 1)
                for char in value:
                    self.code_writer.write_push(Segment.CONST, ord(char))
                    self.code_writer.write_call("String.appendChar", 2)
            else:
                value = self.eat_keyword_or(['true', 'false', 'null', 'this'])
                if value == "true":
                    self.code_writer.write_push(Segment.CONST, 0)
                    self.code_writer.write_arithmetic(Command.NOT)
                elif value == "false":
                    self.code_writer.write_push(Segment.CONST, 0)
                elif value == "null":
                    self.code_writer.write_push(Segment.CONST, 0)
                elif value == "this":
                    self.code_writer.write_push(Segment.POINTER, 0)
        elif next_type == Token.SYMBOL:
            if next_token == "(":
                self.eat_symbol("(")
                self.compile_expression()
                self.eat_symbol(")")
            else:
                value = self.eat_symbol_or(["-", "~"])
                self.compile_term()
                if value == "-":
                    self.code_writer.write_arithmetic(Command.NEG)
                elif value == "~":
                    self.code_writer.write_arithmetic(Command.NOT)
        else:
            iden_name = self.eat_identifier()
            next_token, _ = self.tokenizer.peek()
            if next_token == "[":
                iden_index = self.symbol_table.index_of(iden_name)
                segment = self.segment_map[self.symbol_table.kind_of(iden_name)]
                self.code_writer.write_push(segment, iden_index)

                self.eat_symbol('[')
                self.compile_expression()

                self.code_writer.write_arithmetic(Command.ADD)
                self.code_writer.write_pop(Segment.POINTER, 1)
                self.code_writer.write_push(Segment.THAT, 0)

                self.eat_symbol(']')
            elif next_token in ["(", "."]:
               self.compile_subroutine_call_args_and_body(iden_name) 
            else:
                iden_index = self.symbol_table.index_of(iden_name)
                segment = self.segment_map[self.symbol_table.kind_of(iden_name)]
                self.code_writer.write_push(segment, iden_index)

        print("</term>")

    """
    <subroutineCall> =>
        <subroutineName> '(' <expressionList> ')' |
        (<className>|<varName>) '.' <subroutineName> '(' <expressionList> ')'
    """
    def compile_subroutine_call(self):
        base_iden = self.eat_identifier()
        self.compile_subroutine_call_args_and_body(base_iden)
        
    def compile_subroutine_call_args_and_body(self, base_iden):
        next_token, next_type = self.tokenizer.peek()
        nargs = 0

        # Implicit method
        if next_token == "(":
            self.eat_symbol('(')

            self.code_writer.write_push(Segment.POINTER, 0)

            nargs = self.compile_expression_list()
            self.eat_symbol(')')

            self.code_writer.write_call("{}.{}".format(self.class_name, base_iden), nargs + 1)
        else: # Method or regular call
            self.eat_symbol('.')

            fn_iden = self.eat_identifier()
            base_is_instance = lambda x: x[0].lower() == x[0]

            if base_is_instance(base_iden):
                iden_index = self.symbol_table.index_of(base_iden)
                segment = self.segment_map[self.symbol_table.kind_of(base_iden)]
                self.code_writer.write_push(segment, iden_index)

            self.eat_symbol('(')
            nargs = self.compile_expression_list()
            self.eat_symbol(')')
           
            if base_is_instance(base_iden): 
                base_class_name = self.symbol_table.type_of(base_iden)
                full_name = "{}.{}".format(base_class_name, fn_iden)
                self.code_writer.write_call(full_name, nargs + 1)
            else:
                self.code_writer.write_call(
                    "{}.{}".format(base_iden, fn_iden),
                    nargs 
                )

    """
     <expressionList> =>
     (<expression> (',' <expression>)* )?
    """
    def compile_expression_list(self):
        print("<expressionList>")
        count = 0
        next_token, _ = self.tokenizer.peek()
        if next_token != ")":
            self.compile_expression()
            count += 1
            count += self.compile_expression_zero_or_more()
        print("</expressionList>")
        return count
    
    def compile_expression_zero_or_more(self):
        next_token, _ = self.tokenizer.peek()
        count = 0
        while next_token == ",":
            self.eat_symbol(',')
            self.compile_expression()
            count += 1
            next_token, _ = self.tokenizer.peek()
        return count
        
    def eat_symbol(self, value):
        self.tokenizer.advance()
        if self.tokenizer.symbol() != value:
            raise RuntimeError("Missing symbol: {}".format(value))
        print(self.tokenizer.xml())
        return self.tokenizer.symbol()

    def eat_integer(self):
        self.tokenizer.advance()
        if self.tokenizer.token_type() != Token.INT_CONSTANT:
            raise RuntimeError("Missing integer")
        print(self.tokenizer.xml())
        return self.tokenizer.int_value()

    def eat_string(self):
        self.tokenizer.advance()
        if self.tokenizer.token_type() != Token.STRING_CONSTANT:
            raise RuntimeError("Missing string")
        print(self.tokenizer.xml())
        return self.tokenizer.string_value()

    def eat_keyword(self, value):
        self.tokenizer.advance()
        if self.tokenizer.key_word() != value:
            raise RuntimeError("Missing keyword: {}".format(value))
        print(self.tokenizer.xml())
        return self.tokenizer.key_word()

    def eat_keyword_or(self, values):
        self.tokenizer.advance()
        if self.tokenizer.key_word() not in values:
            raise RuntimeError("Missing keywords: {}".format(values))
        print(self.tokenizer.xml())
        return self.tokenizer.key_word()

    def eat_symbol_or(self, values):
        self.tokenizer.advance()
        if self.tokenizer.symbol() not in values:
            raise RuntimeError("Missing symbols: {}".format(values))
        print(self.tokenizer.xml())
        return self.tokenizer.symbol()

    def eat_identifier(self):
        self.tokenizer.advance()
        if self.tokenizer.token_type() != Token.IDENTIFIER:
            raise RuntimeError("Missing identifier")
        print(self.tokenizer.xml())
        return self.tokenizer.identifier()

def read_files(folder_path):
    file_list = os.listdir(folder_path)
    files = [os.path.join(folder_path, file_name) for file_name in file_list if ".jack" in file_name]
    return files

def compile_file(filename):
    with open(filename, 'r') as f:
        try:
            engine = JackCompilationEngine(f.read())
            engine.compile_class()
            vm_name = filename.split('/')[-1].split('.')[0] + ".vm"
        except: 
            print("Failed to compile {}".format(filename))
            raise
        with open(vm_name, 'w') as k:
            output = engine.code_writer.output()
            k.write(output)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("You need to supply an input file")

    filename = sys.argv[1]
    if os.path.isdir(filename):
        files = read_files(filename)
        for file_name in files:
            compile_file(file_name)
    else:
        compile_file(filename)

