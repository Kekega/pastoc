import pickle
from functools import wraps

from nodes import *
from token_class import Class


class ParsingError(Exception):
    # Класс исключения для ошибок при парсинге
    def __init__(self, element="", comm=""):
        self.message = f"Parsing error while parsing element {element}."
        if comm:
            self.message += " " + comm
        super().__init__(self.message)


class Parser:
    # Класс парсера
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = tokens.pop(0)
        self.prev = None

    error_message = ""
    
    def eat(self, class_):
        print(self.curr.class_)
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.tokens.pop(0)
        else:
            self.die_type(class_.name, self.curr.class_.name)

    def program(self):
        # <program> ::= (<proc> | <func> | "var" <variables> | <main_program>) <EOF>
        # <main_program> ::= "begin" <block> "end" "."
        nodes = []
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.proc())
            elif self.curr.class_ == Class.FUNCTION:
                nodes.append(self.func())
            elif self.curr.class_ == Class.VAR:
                self.eat(Class.VAR)
                vars= self.variables()
                nodes.append(vars)
            elif self.curr.class_ == Class.BEGIN:
                self.eat(Class.BEGIN)
                nodes.append(self.block(multiline=True))
                self.eat(Class.END)
                self.eat(Class.DOT)
            else:
                self.die_deriv(self.program.__name__)
        return Program(nodes)

    def parVars(self, parent = '_'): 
        # <parVars> ::= (<id> ("," <id>)* ":" <type>)*
        vars = []
        lista = []
        while self.curr.class_ != Class.RPAREN:
            if (self.curr.class_ == Class.ID):
                lista.append(self.curr.lexeme)
                self.eat(Class.ID)
            
                while (self.curr.class_ == Class.COMMA):
                    self.eat(Class.COMMA)
                    if self.curr.class_ == Class.ID:
                        lista.append(self.curr.lexeme)
                        self.eat(Class.ID)
                    else:
                        self.die_deriv("parVars")

                if (self.curr.class_ == Class.COLON):
                    self.eat(Class.COLON)
                    tip = self.type_()
                    for x in lista:
                        id = Id(x)
                        vars.append(Decl(tip, id))

                    lista.clear()
                    if self.curr.class_ != Class.RPAREN:
                        self.eat(Class.SEMICOLON)
                else:
                    self.die_deriv("parVars")
                
            else:
                self.die_deriv("parVars")

        return Params(vars)

    def variables(self, parent='_'):
        # variables = (ID ("," ID)* ":" (type | <array_decl>) ";")*
        # <array_decl> ::= "array" "[" <INT> "." "." <INT> "]" "of" <type>
        vars = []
        ids_list = []

        while self.curr.class_ == Class.ID:

            if (self.curr.class_ == Class.ID):
                ids_list.append(self.curr.lexeme)
                self.eat(Class.ID)

                while (self.curr.class_ == Class.COMMA):
                    self.eat(Class.COMMA)
                    if (self.curr.class_ == Class.ID):
                        ids_list.append(self.curr.lexeme)
                        self.eat(Class.ID)
                    else:
                        self.die_deriv("variables")

                if (self.curr.class_ == Class.COLON):
                    self.eat(Class.COLON)

                    if self.curr.class_ == Class.TYPE:
                        tip = self.type_()
                        for x in ids_list:
                            id = Id(x)
                            vars.append(Decl(tip, id))
                            
                        self.eat(Class.SEMICOLON)

                    elif self.curr.class_ == Class.ARRAY:
                        self.eat(Class.ARRAY)
                        self.eat(Class.LBRACKET)
                        low = Int(self.curr.lexeme)
                        self.eat(Class.INT)
                        self.eat(Class.DOT)
                        self.eat(Class.DOT)
                        high = Int(self.curr.lexeme)
                        self.eat(Class.INT)
                        self.eat(Class.RBRACKET)
                        self.eat(Class.OF)
                        tip = self.type_()
                        elements = None

                        for x in ids_list:
                            vars.append(ArrayDecl(tip, Id(x), low, high, elements))
                        self.eat(Class.SEMICOLON)
                    ids_list.clear()
            
                    
        print(self.curr.class_)

        return Variables(vars)

    def proc(self):
        # <proc> ::= "procedure" <id> "(" <parVars> ")" ";" ("var" <variables>)?
        #                               (<func> <proc>)* "begin" <block> "end" ";"
        try:
            self.eat(Class.PROCEDURE)
            id_ = self.idDefines()
            self.eat(Class.LPAREN)
            params = self.parVars(id_)
            self.eat(Class.RPAREN)
            self.eat(Class.SEMICOLON)
            vars = []
            fs, prs = [], []
            if self.curr.class_ == Class.VAR:
                self.eat(Class.VAR)
                vars = self.variables()
            
            if not vars:
                vars = Variables(vars)
            
            while self.curr.class_ != Class.BEGIN:
                if (self.curr.class_ == Class.FUNCTION):
                    fs.append(self.func())
                
                elif (self.curr.class_ == Class.PROCEDURE):
                    prs.append(self.proc())


            self.eat(Class.BEGIN)
            block = self.block(multiline=True, fs=fs, prs=prs)
            self.eat(Class.END)
            self.eat(Class.SEMICOLON)

            return ProcImpl(id_, params, block, vars)
        except Exception:
            raise ParsingError(f"procedure. {self.error_message}")

    def func(self):
        # <func> ::= "function" <id> "(" <parVars> ")" ":" <type> ";" ("var" <variables>)?
        #                       (<func> <proc>)* "begin" <block> "end" ";"
        try:
            self.eat(Class.FUNCTION)
            id_ = self.idDefines()
            self.eat(Class.LPAREN)
            params = self.parVars(id_)
            self.eat(Class.RPAREN)
            self.eat(Class.COLON)
            type_ = Type(self.curr.lexeme)
            self.eat(Class.TYPE)
            self.eat(Class.SEMICOLON)
            vars = []
            fs, prs = [], []

            if self.curr.class_ == Class.VAR:
                self.eat(Class.VAR)
                vars = self.variables()
            
            if not vars:
                vars = Variables(vars)
            
            while self.curr.class_ != Class.BEGIN:
                if (self.curr.class_ == Class.FUNCTION):
                    fs.append(self.func())
                
                elif (self.curr.class_ == Class.PROCEDURE):
                    prs.append(self.proc())            

            self.eat(Class.BEGIN)
            block = self.block(multiline=True, fs=fs, prs=prs)
            self.eat(Class.END)
            self.eat(Class.SEMICOLON)
            return FuncImpl(type_, id_, params, block, vars)
        except Exception:
            raise ParsingError(f"function. {self.error_message}")
        

    def id_(self):
        # <id_> ::= <FuncProcCall> | <ArrayElem> | <Assign> | <id>
        # <FuncProcCall> ::= <id> "(" <args> ")"
        # <ArrayElem> ::= <id> "[" <compare> "]"
        # <Assign> ::= <id> ":=" <compare>
        is_array_elem = self.prev.class_ != Class.TYPE
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            return FuncProcCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET and is_array_elem:
            self.eat(Class.LBRACKET)
            index = self.expr()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            compare = self.compare()
            return Assign(id_, compare)
        else:
            return id_

    def idDefines(self):
        # <id>
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        return id_

    def if_(self):
        # <if> ::= "if" <compare> "then" (<statement> | "begin" <statement>* "end") 
                    #   (("else" (<statement> | "begin" <statement>* "end" ";")) | ";")
        self.eat(Class.IF)
        cond = self.compare()
        self.eat(Class.THEN)

        f = False
        if self.curr.class_ == Class.BEGIN:
            self.eat(Class.BEGIN)
            true = self.block(multiline=True)
            self.eat(Class.END)
            f = True
        else:
            true = self.block(multiline=False)
        false = None
        if self.curr.class_ == Class.ELSE:
            self.eat(Class.ELSE)
            if self.curr.class_ == Class.BEGIN:
                self.eat(Class.BEGIN)
                false = self.block(multiline=True)
                self.eat(Class.END)
                self.eat(Class.SEMICOLON)
            else:
                t = False
                false = self.block(multiline=False)
        if f:
            self.eat(Class.SEMICOLON)
        return If(cond, true, false)

    def while_(self): 
        # <while> ::= "while" <compare> "do" (<statement> | "begin" <statement>* "end" ";"?)
        self.eat(Class.WHILE)
        cond = self.compare()
        self.eat(Class.DO)
        if self.curr.class_ == Class.BEGIN:
            self.eat(Class.BEGIN)
            block = self.block(multiline=True)
            self.eat(Class.END)
            if (self.curr.class_ == Class.SEMICOLON):
                self.eat(Class.SEMICOLON)
        else:
            block = self.block(multiline=False)
        return While(cond, block)
    
    def assign(self):
        # <assign> ::= <id> ":=" <compare>
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        self.eat(Class.ASSIGN)
        compare = self.compare()
        return Assign(id_, compare)

    def for_(self):
        # <for> ::= "for" <assign> ("to" | "downto") <expr> "do" (<statement> | "begin" <statement>* "end" ";")
        self.eat(Class.FOR)
        init = self.assign()
        if self.curr.class_ == Class.TO:
            self.eat(Class.TO)
            where = 'to'
        elif self.curr.class_ == Class.DOWNTO:
            self.eat(Class.DOWNTO)
            where = 'downto'
        else:
            self.die_deriv("for")
        expr = self.expr()
        self.eat(Class.DO)
        if self.curr.class_ == Class.BEGIN:
            self.eat(Class.BEGIN)
            block = self.block(multiline=True)
            self.eat(Class.END)
            self.eat(Class.SEMICOLON)
        else:
            block = self.block(multiline=False)
        return For(init, expr, block, Where(where))

    def repeat(self):
        # <repeat> ::= "repeat" <statement>* "until" <compare> ";"
        self.eat(Class.REPEAT)
        block = self.block(multiline=True, repeat=True)
        self.eat(Class.UNTIL)
        cond = self.compare()
        self.eat(Class.SEMICOLON)
        return RepeatUntil(cond, block)

    def statement(self):
        # <statement> ::= (<if> | <while> | <for> | <repeat> | <id_> ";")
        if self.curr.class_ == Class.IF:
            return self.if_()
        elif self.curr.class_ == Class.WHILE:
            return self.while_()
        elif self.curr.class_ == Class.FOR:
            return self.for_()
        elif self.curr.class_ == Class.REPEAT:
            return self.repeat()
        elif self.curr.class_ == Class.ID:
            id = self.id_()
            self.eat(Class.SEMICOLON)
            return id
        else:
            self.die_deriv(self.block.__name__)

    def block(self, multiline: bool, fs = None, prs = None, repeat: bool = False):
        nodes = []
        if fs:
            for new_func in fs:
                nodes.append(new_func)
        if prs:
            for new_proc in prs:
                nodes.append(new_proc)

        if multiline:
            end_cond = Class.END if not repeat else Class.UNTIL

            while self.curr.class_ != end_cond:
                nodes.append(self.statement())
        else:
            nodes.append(self.statement())
        return Block(nodes)

    def params(self):
        # <params> ::= <variables>*
        params = []
        while self.curr.class_ != Class.RPAREN:
            vars, _, _ = self.variables()
            params.append(vars)

        return Params(params)

    def args(self):
        # <args> ::= <compare> (":" <expr> ":" <expr>)? ("," <compare> (":" <expr> ":" <expr>)?)*
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            expr = self.compare()

            if (self.curr.class_ == Class.COLON):
                self.eat(Class.COLON)
                left = self.expr()
                self.eat(Class.COLON)
                right = self.expr()
                args.append(FormattedArg(expr, left, right))
            else:
                args.append(expr)

        return Args(args)

    def type_(self):
        # <type>
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        return type_

    def factor(self):
        # <factor> ::= <int> | <char> | <string> | <boolean> | <real> | <id_> | 
        #            ("-" | "not") ("(" <compare> ")" | <factor>) | "(" <compare> ")"
        if self.curr.class_ == Class.INT:
            value = Int(self.curr.lexeme)
            self.eat(Class.INT)
            return value
        elif self.curr.class_ == Class.CHAR:
            value = Char(self.curr.lexeme)
            self.eat(Class.CHAR)
            return value
        elif self.curr.class_ == Class.STRING:
            value = String(self.curr.lexeme)
            self.eat(Class.STRING)
            return value
        elif self.curr.class_ == Class.BOOLEAN:
            value = Boolean(self.curr.lexeme)
            self.eat(Class.BOOLEAN)
            return value
        elif self.curr.class_ == Class.REAL:
            value = Real(self.curr.lexeme)
            self.eat(Class.REAL)
            return value
        elif self.curr.class_ == Class.ID:
            return self.id_()
        elif self.curr.class_ in [Class.MINUS, Class.NOT]:
            op = self.curr
            self.eat(self.curr.class_)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.compare()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.compare()
            self.eat(Class.RPAREN)
            return first
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        # <term> ::= <factor> (("*" | "/" | "mod" | "div" | "and") <factor>)*
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.FWDSLASH, Class.MOD, Class.DIV, Class.AND]:
            if self.curr.class_ == Class.STAR:
                op = self.curr.lexeme
                self.eat(Class.STAR)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.FWDSLASH:
                op = self.curr.lexeme
                self.eat(Class.FWDSLASH)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MOD:
                op = self.curr.lexeme
                self.eat(Class.MOD)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.DIV:
                op = self.curr.lexeme
                self.eat(Class.DIV)
                second = self.factor()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.AND:
                op = self.curr.lexeme
                self.eat(Class.AND)
                second = self.factor()
                first = BinOp(op, first, second)
        return first

    def expr(self):
        # <expr> ::= <term> (("+" | "-" | "or" | "xor") <term>)*
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS, Class.OR, Class.XOR]:
            if self.curr.class_ == Class.PLUS:
                op = self.curr.lexeme
                self.eat(Class.PLUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.MINUS:
                op = self.curr.lexeme
                self.eat(Class.MINUS)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.OR:
                op = self.curr.lexeme
                self.eat(Class.OR)
                second = self.term()
                first = BinOp(op, first, second)
            elif self.curr.class_ == Class.XOR:
                op = self.curr.lexeme
                self.eat(Class.XOR)
                second = self.term()
                first = BinOp(op, first, second)
        return first

    def compare(self):
        # <compare> ::= <expr> (("=" | "<>" | "<" | ">" | "<=" | ">=") <expr>)?
        first = self.expr()
        if self.curr.class_ == Class.EQSIGN:
            op = self.curr.lexeme
            self.eat(Class.EQSIGN)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.NEQ:
            op = self.curr.lexeme
            self.eat(Class.NEQ)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LT:
            op = self.curr.lexeme
            self.eat(Class.LT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GT:
            op = self.curr.lexeme
            self.eat(Class.GT)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.LTE:
            op = self.curr.lexeme
            self.eat(Class.LTE)
            second = self.expr()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.GTE:
            op = self.curr.lexeme
            self.eat(Class.GTE)
            second = self.expr()
            return BinOp(op, first, second)
        else:
            return first

    def parse(self):
        return self.program()

    def die(self, text):
        self.error_message = text
        raise ValueError(self.error_message)

    def die_deriv(self, fun):
        self.die(f"Derivation error: {fun} {self.curr} (row:{self.curr.row}, col:{self.curr.col})")

    def die_type(self, expected, found):
        self.die(f"Expected: {expected}, Found: {found} (row:{self.curr.row}, col:{self.curr.col})")
