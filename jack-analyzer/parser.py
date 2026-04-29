import re
import os

# --- 1. THE TOKENIZER (The "Word" Finder) ---
class JackTokenizer:
    KEYWORDS = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}
    SYMBOLS = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}

    def __init__(self, filename):
        with open(filename, 'r') as f:
            code = f.read()
        # Remove comments
        code = re.sub(r'/\*.*?\*/', ' ', code, flags=re.DOTALL)
        code = re.sub(r'//.*?\n', '\n', code)
        # Tokenize
        pattern = r'"[^"\n]*"|' + '|'.join(map(re.escape, self.SYMBOLS)) + r'|\d+|[\w_]+'
        self.tokens = re.findall(pattern, code)
        self.pos = -1
        self.current_token = None

    def has_more(self):
        return (self.pos + 1) < len(self.tokens)

    def advance(self):
        if self.has_more():
            self.pos += 1
            self.current_token = self.tokens[self.pos]
    
    def peek(self):
        if self.has_more(): return self.tokens[self.pos + 1]
        return None

    def token_type(self):
        if self.current_token in self.KEYWORDS: return "keyword"
        if self.current_token in self.SYMBOLS: return "symbol"
        if self.current_token.isdigit(): return "integerConstant"
        if self.current_token.startswith('"'): return "stringConstant"
        return "identifier"

# --- 2. THE PARSER (The "Structure" Builder) ---
class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.t = tokenizer
        self.out = open(output_file, 'w')
        self.indent = 0

    def write_tag(self, text):
        self.out.write("  " * self.indent + text + "\n")

    def process(self):
        """Moves to next token and writes it as a leaf in the XML tree."""
        self.t.advance()
        tag = self.t.token_type()
        val = self.t.current_token
        if tag == "stringConstant": val = val[1:-1]
        val = val.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        self.write_tag(f"<{tag}> {val} </{tag}>")

    def compile_class(self):
        self.write_tag("<class>")
        self.indent += 1
        self.process() # 'class'
        self.process() # className
        self.process() # '{'
        while self.t.peek() in ['static', 'field']: self.compile_class_var_dec()
        while self.t.peek() in ['constructor', 'function', 'method']: self.compile_subroutine()
        self.process() # '}'
        self.indent -= 1
        self.write_tag("</class>")
        self.out.close()

    def compile_class_var_dec(self):
        self.write_tag("<classVarDec>")
        self.indent += 1
        while self.t.peek() != ';': self.process()
        self.process() # ';'
        self.indent -= 1
        self.write_tag("</classVarDec>")

    def compile_subroutine(self):
        self.write_tag("<subroutineDec>")
        self.indent += 1
        for _ in range(3): self.process() # (type) name
        self.process() # '('
        self.compile_parameter_list()
        self.process() # ')'
        # Subroutine Body
        self.write_tag("<subroutineBody>")
        self.indent += 1
        self.process() # '{'
        while self.t.peek() == 'var': self.compile_var_dec()
        self.compile_statements()
        self.process() # '}'
        self.indent -= 1
        self.write_tag("</subroutineBody>")
        self.indent -= 1
        self.write_tag("</subroutineDec>")

    def compile_parameter_list(self):
        self.write_tag("<parameterList>")
        self.indent += 1
        while self.t.peek() != ')': self.process()
        self.indent -= 1
        self.write_tag("</parameterList>")

    def compile_var_dec(self):
        self.write_tag("<varDec>")
        self.indent += 1
        while self.t.peek() != ';': self.process()
        self.process() # ';'
        self.indent -= 1
        self.write_tag("</varDec>")

    def compile_statements(self):
        self.write_tag("<statements>")
        self.indent += 1
        while self.t.peek() in ['let', 'if', 'while', 'do', 'return']:
            curr = self.t.peek()
            if curr == 'let': self.compile_let()
            elif curr == 'if': self.compile_if()
            elif curr == 'while': self.compile_while()
            elif curr == 'do': self.compile_do()
            elif curr == 'return': self.compile_return()
        self.indent -= 1
        self.write_tag("</statements>")

    def compile_let(self):
        self.write_tag("<letStatement>")
        self.indent += 1
        self.process() # 'let'
        self.process() # varName
        if self.t.peek() == '[':
            self.process() # '['
            self.compile_expression()
            self.process() # ']'
        self.process() # '='
        self.compile_expression()
        self.process() # ';'
        self.indent -= 1
        self.write_tag("</letStatement>")

    def compile_do(self):
        self.write_tag("<doStatement>")
        self.indent += 1
        while self.t.peek() != '(': self.process()
        self.process() # '('
        self.compile_expression_list()
        self.process() # ')'
        self.process() # ';'
        self.indent -= 1
        self.write_tag("</doStatement>")

    def compile_expression(self):
        self.write_tag("<expression>")
        self.indent += 1
        self.compile_term()
        ops = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
        while self.t.peek() in ops:
            self.process() # op
            self.compile_term()
        self.indent -= 1
        self.write_tag("</expression>")

    def compile_term(self):
        self.write_tag("<term>")
        self.indent += 1
        peek = self.t.peek()

        if peek == '(':
            self.process() # '('
            self.compile_expression()
            self.process() # ')'
        elif peek in ['-', '~']: # Unary ops
            self.process()
            self.compile_term()
        else:
            self.process() # varName, className, subroutineName, constant

            if self.t.peek() == '[':
                self.process() # '['
                self.compile_expression()
                self.process() # ']'
            elif self.t.peek() == '(':
                self.process() # '('
                self.compile_expression_list()
                self.process() # ')'
            elif self.t.peek() == '.':
                self.process() # '.'
                self.process() # subroutineName
                self.process() # '('
                self.compile_expression_list()
                self.process() # ')'
        self.indent -= 1
        self.write_tag("</term>")

    def compile_expression_list(self):
        self.write_tag("<expressionList>")
        self.indent += 1
        if self.t.peek() != ')':
            self.compile_expression()
            while self.t.peek() == ',':
                self.process() # ','
                self.compile_expression()
        self.indent -= 1
        self.write_tag("</expressionList>")

    # If, While, Return follow similar patterns
    def compile_if(self):
        self.write_tag("<ifStatement>")
        self.indent += 1
        self.process(); self.process() # 'if' '('
        self.compile_expression()
        self.process(); self.process() # ')' '{'
        self.compile_statements()
        self.process() # '}'
        if self.t.peek() == 'else':
            self.process(); self.process() # 'else' '{'
            self.compile_statements()
            self.process() # '}'
        self.indent -= 1
        self.write_tag("</ifStatement>")

    def compile_while(self):
        self.write_tag("<whileStatement>")
        self.indent += 1
        self.process(); self.process() # 'while' '('
        self.compile_expression()
        self.process(); self.process() # ')' '{'
        self.compile_statements()
        self.process() # '}'
        self.indent -= 1
        self.write_tag("</whileStatement>")

    def compile_return(self):
        self.write_tag("<returnStatement>")
        self.indent += 1
        self.process() # 'return'
        if self.t.peek() != ';': self.compile_expression()
        self.process() # ';'
        self.indent -= 1
        self.write_tag("</returnStatement>")

# --- 3. MAIN RUNNER ---
def main():
    for filename in os.listdir('.'):
        if filename.endswith(".jack") and os.path.isfile(filename):
            tokenizer = JackTokenizer(filename)
            output_xml = filename.replace(".jack", ".xml")
            engine = CompilationEngine(tokenizer, output_xml)
            engine.compile_class()
            print(f"Success! Generated {output_xml}")

if __name__ == "__main__":
    main()
