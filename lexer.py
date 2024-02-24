from curses.ascii import isdigit

from token_class import Class
from tokens import Token


class Lexer:
    def __init__(self, text):
        self.text = text
        self.len = len(text)
        self.pos = -1
        self.row = 1 
        self.col = 1 

    def read_space(self):
        # Чтение пробелов и учет перевода строки
        while self.pos + 1 < self.len and self.text[self.pos + 1].isspace():
            if self.text[self.pos + 1] == '\n':
                self.row += 1
                self.col = 0
            self.next_char()

    def read_int(self):
        # Чтение цифр для формирования целого числа
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.next_char()

        return int(lexeme)

    def read_real(self):
        # Чтение цифр для формирования вещественного числа
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.next_char()
        lexeme += self.next_char()
        while self.pos + 1 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.next_char()

        return float(lexeme)

    def read_number(self):
        # Чтение цифр для формирования числа (целого или вещественного)
        lexeme = self.text[self.pos]
        while self.pos + 2 < self.len and self.text[self.pos + 1].isdigit():
            lexeme += self.next_char()
        test = self.text[self.pos + 1]
        test1 = self.text[self.pos + 2]
        if test == '.' and test1.isnumeric():
            lexeme += self.next_char()
            while self.pos + 2 < self.len and self.text[self.pos + 1].isdigit():
                lexeme += self.next_char()
            return float(lexeme)
        else:
            return int(lexeme)

    def read_char(self):
        # Чтение одного символа
        self.pos += 1
        lexeme = self.text[self.pos]
        self.pos += 1
        return lexeme

    def read_string(self):
        # Чтение строки внутри одинарных кавычек
        lexeme = ''
        while self.pos + 1 < self.len and self.text[self.pos + 1] != '\'':
            lexeme += self.next_char()
        self.pos += 1
        return lexeme

    def read_keyword(self):
        # Чтение ключевых слов
        lexeme = self.text[self.pos]
        while self.pos + 1 < self.len and self.text[self.pos + 1].isalnum() or self.text[self.pos + 1] == '_':
            lexeme += self.next_char()
        if lexeme == 'if':
            return Token(Class.IF, lexeme, self.row, self.col)
        elif lexeme == 'else':
            return Token(Class.ELSE, lexeme, self.row, self.col)
        elif lexeme == 'while':
            return Token(Class.WHILE, lexeme, self.row, self.col)
        elif lexeme == 'for':
            return Token(Class.FOR, lexeme, self.row, self.col)
        # elif lexeme == 'break':
        #     return Token(Class.BREAK, lexeme, self.row, self.col)
        # elif lexeme == 'continue':
        #     return Token(Class.CONTINUE, lexeme, self.row, self.col)
        elif lexeme == 'integer' or lexeme == 'char':
            return Token(Class.TYPE, lexeme, self.row, self.col)
        elif lexeme == 'begin':
            return Token(Class.BEGIN, lexeme, self.row, self.col)
        elif lexeme == 'end':
            return Token(Class.END, lexeme, self.row, self.col)
        elif lexeme == 'var':
            return Token(Class.VAR, lexeme, self.row, self.col)
        elif lexeme == 'procedure':
            return Token(Class.PROCEDURE, lexeme, self.row, self.col)
        elif lexeme == 'function':
            return Token(Class.FUNCTION, lexeme, self.row, self.col)
        elif lexeme == 'to':
            return Token(Class.TO, lexeme, self.row, self.col)
        elif lexeme == 'do':
            return Token(Class.DO, lexeme, self.row, self.col)
        elif lexeme == 'program':
            return Token(Class.PROGRAM, lexeme, self.row, self.col)
        elif lexeme == 'array':
            return Token(Class.ARRAY, lexeme, self.row, self.col)
        elif lexeme == 'of':
            return Token(Class.OF, lexeme, self.row, self.col)
        elif lexeme == 'then':
            return Token(Class.THEN, lexeme, self.row, self.col)
        elif lexeme == 'mod':
            return Token(Class.MOD, lexeme, self.row, self.col)
        elif lexeme == 'div':
            return Token(Class.DIV, lexeme, self.row, self.col)
        elif lexeme == 'or':
            return Token(Class.OR, lexeme, self.row, self.col)
        elif lexeme == 'real':
            return Token(Class.TYPE, lexeme, self.row, self.col)
        elif lexeme == 'const':
            return Token(Class.CONST, lexeme, self.row, self.col)
        elif lexeme == 'and':
            return Token(Class.AND, lexeme, self.row, self.col)
        elif lexeme == 'case':
            return Token(Class.CASE, lexeme, self.row, self.col)
        elif lexeme == 'in':
            return Token(Class.IN, lexeme, self.row, self.col)
        elif lexeme == 'nil':
            return Token(Class.NIL, lexeme, self.row, self.col)
        elif lexeme == 'repeat':
            return Token(Class.REPEAT, lexeme, self.row, self.col)
        elif lexeme == 'until':
            return Token(Class.UNTIL, lexeme, self.row, self.col)
        elif lexeme == 'boolean':
            return Token(Class.TYPE, lexeme, self.row, self.col)
        elif lexeme == 'xor':
            return Token(Class.XOR, lexeme, self.row, self.col)
        elif lexeme == 'string':
            return Token(Class.TYPE, lexeme, self.row, self.col)
        elif lexeme == 'downto':
            return Token(Class.DOWNTO, lexeme, self.row, self.col)
        elif lexeme == 'true':
            return Token(Class.TRUE, lexeme, self.row, self.col)
        elif lexeme == 'false':
            return Token(Class.FALSE, lexeme, self.row, self.col)
        elif lexeme == 'true' or lexeme == 'false':
            return Token(Class.BOOLEAN, lexeme, self.row, self.col)
        if isdigit(lexeme[0]):
            raise ValueError("Variable names can not start with digits: {lexeme}, ({self.row}, {self.col})")
        return Token(Class.ID, lexeme, self.row, self.col)

    def next_char(self):
        # Переход к следующему символу
        self.pos += 1
        self.col += 1
        if self.pos >= self.len:
            return None
        return self.text[self.pos]
    
    def skip_comment(self):

        self.read_space()

        ch = self.next_char()
        if not ch:
            raise ValueError("No EOF token")
        eaten = ch
        while '}' not in eaten and '*)' not in eaten:
            self.read_space()
            
            ch = self.next_char()
            if not ch:
                raise ValueError("No EOF Token")
            eaten += ch
        self.read_space()
        
    def next_token(self):
        # Получение следующего токена
        self.read_space()
        curr = self.next_char()
        if curr is None:
            return Token(Class.EOF, curr, self.row, self.col)
        token = None
        if curr.isalpha() or curr == '_':
            token = self.read_keyword()
        elif curr.isdigit():
            number = self.read_number()
            if isinstance(number, int):
                token = Token(Class.INT, number, self.row, self.col)
            elif isinstance(number, float):
                token = Token(Class.REAL, number, self.row, self.col)
        elif curr == '\'':
            lexeme = self.read_string()
            if len(lexeme) == 1:
                token = Token(Class.CHAR, lexeme, self.row, self.col)
            else:
                token = Token(Class.STRING, lexeme, self.row, self.col)
        elif curr == '+':
            token = Token(Class.PLUS, curr, self.row, self.col)
        elif curr == '-':
            token = Token(Class.MINUS, curr, self.row, self.col)
        elif curr == '*':
            token = Token(Class.STAR, curr, self.row, self.col)
        elif curr == '/':
            token = Token(Class.FWDSLASH, curr, self.row, self.col)
        elif curr == '%':
            token = Token(Class.PERCENT, curr, self.row, self.col)
        elif curr == '|':
            curr = self.next_char()
            if curr == '|':
                token = Token(Class.OR, '||', self.row, self.col)
            else:
                self.die(curr)
        elif curr == '!':
            curr = self.next_char()
            token = Token(Class.NOT, '!', self.row, self.col)
        elif curr == '=':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.EQ, '==', self.row, self.col)
            else:
                token = Token(Class.EQSIGN, '=', self.row, self.col)
        elif curr == '<':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.LTE, '<=', self.row, self.col)
            elif curr == ">":
                token = Token(Class.NEQ, "<>", self.row, self.col)
            else:
                token = Token(Class.LT, '<', self.row, self.col)
                self.pos -= 1
        elif curr == '>':
            curr = self.next_char()
            if curr == '=':
                token = Token(Class.GTE, '>=', self.row, self.col)
            else:
                token = Token(Class.GT, '>', self.row, self.col)
                self.pos -= 1
        elif curr == '(':
            if self.text[self.pos + 1] == '*':
                self.skip_comment()
                token = self.next_token()
            else:
                token = Token(Class.LPAREN, curr, self.row, self.col)
        elif curr == ')':
            token = Token(Class.RPAREN, curr, self.row, self.col)
        elif curr == '[':
            token = Token(Class.LBRACKET, curr, self.row, self.col)
        elif curr == ']':
            token = Token(Class.RBRACKET, curr, self.row, self.col)
        elif curr == '{':
            self.skip_comment()
            token = self.next_token()
            # token = Token(Class.LBRACE, curr, self.row, self.col)
        elif curr == '}':
            token = Token(Class.RBRACE, curr, self.row, self.col)
        elif curr == ';':
            token = Token(Class.SEMICOLON, curr, self.row, self.col)
        elif curr == ',':
            token = Token(Class.COMMA, curr, self.row, self.col)
        elif curr == '.':
            token = Token(Class.DOT, curr, self.row, self.col)
        elif curr == ':':
            token = Token(Class.COLON, curr, self.row, self.col)
            curr = self.text[self.pos + 1]
            if curr == '=':
                token = Token(Class.ASSIGN, ':=', self.row, self.col)
                self.next_char()
        else:
            self.die(curr)
        return token

    def lex(self):
        tokens = []
        while True:
            curr = self.next_token()
            tokens.append(curr)
            if curr.class_ == Class.EOF:
                break
        return tokens

    def die(self, char):
        # Обработка ошибки некорректного символа
        raise ValueError(f"Unexpected character: {char}. (row:{self.row}, col:{self.col})")
