import pickle
from functools import wraps

from nodes import *
from token_class import Class


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = tokens.pop(0)
        self.prev = None

    def restorable(call):
        @wraps(call)
        def wrapper(self, *args, **kwargs):
            state = pickle.dumps(self.__dict__)
            result = call(self, *args, **kwargs)
            self.__dict__ = pickle.loads(state)
            return result

        return wrapper

    def eat(self, class_):
        if self.curr.class_ == class_:
            self.prev = self.curr
            self.curr = self.tokens.pop(0)
        else:
            self.die_type(class_.name, self.curr.class_.name)

    def program(self):
        nodes = []
        while self.curr.class_ != Class.EOF:
            if self.curr.class_ == Class.PROCEDURE:
                nodes.append(self.proc())
            elif self.curr.class_ == Class.FUNCTION:
                nodes.append(self.func())
            elif self.curr.class_ == Class.VAR:
                self.eat(Class.VAR)
                nodes.append(self.variables())
            elif self.curr.class_ == Class.BEGIN:
                self.eat(Class.BEGIN)
                nodes.append(self.block())
                self.eat(Class.END)
                self.eat(Class.DOT)
            else:
                self.die_deriv(self.program.__name__)
        return Program(nodes)

    def paramsVar(self):
        vars = []
        lista = []
        while self.curr.class_ != Class.RPAREN:
            if (self.curr.class_ == Class.ID):
                lista.append(self.curr.lexeme)
                self.eat(Class.ID)

            elif (self.curr.class_ == Class.COMMA):
                self.eat(Class.COMMA)

            elif (self.curr.class_ == Class.COLON):
                self.eat(Class.COLON)
                tip = self.type_()
                for x in lista:
                    id = Id(x)
                    vars.append(Decl(tip, id))

                lista.clear()

            if self.curr.class_ == Class.SEMICOLON:
                self.eat(Class.SEMICOLON)

        return Params(vars)

    def variables(self):
        vars = []
        lista = []
        # prev = None
        while self.curr.class_ != Class.BEGIN:
            if (self.curr.class_ == Class.ID):
                lista.append(self.curr.lexeme)
                self.eat(Class.ID)

            elif (self.curr.class_ == Class.COMMA):
                self.eat(Class.COMMA)

            elif (self.curr.class_ == Class.COLON):
                self.eat(Class.COLON)

                if self.curr.class_ == Class.TYPE:
                    tip = self.type_()
                    for x in lista:
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
                    elems = None

                    if self.curr.class_ == Class.SEMICOLON:
                        for x in lista:
                            vars.append(ArrayDecl(tip, Id(x), low, high, elems))
                        self.eat(Class.SEMICOLON)
                    elif (self.curr.class_ == Class.EQSIGN):
                        self.eat(Class.EQSIGN)
                        self.eat(Class.LPAREN)
                        elems = self.elems()
                        self.eat(Class.RPAREN)
                        self.eat(Class.SEMICOLON)
                        vars.append(ArrayDecl(tip, Id(lista[0]), low, high, elems))

                lista.clear()

        return Variables(vars)

    def proc(self):
        self.eat(Class.PROCEDURE)
        id_ = self.idDefines()
        self.eat(Class.LPAREN)
        params = self.paramsVar()
        self.eat(Class.RPAREN)
        self.eat(Class.SEMICOLON)
        vars = []
        if (self.curr.class_ == Class.VAR):
            self.eat(Class.VAR)
            vars = self.variables()
        if not vars:
            vars = Variables(vars)
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        self.eat(Class.SEMICOLON)

        return ProcImpl(id_, params, block, vars)

    def func(self):
        self.eat(Class.FUNCTION)
        id_ = self.idDefines()
        self.eat(Class.LPAREN)
        params = self.paramsVar()
        self.eat(Class.RPAREN)
        self.eat(Class.COLON)
        type_ = Type(self.curr.lexeme)
        self.eat(Class.TYPE)
        self.eat(Class.SEMICOLON)
        vars = []
        if (self.curr.class_ == Class.VAR):
            self.eat(Class.VAR)
            vars = self.variables()
        if not vars:
            vars = Variables(vars)
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        self.eat(Class.SEMICOLON)
        return FuncImpl(type_, id_, params, block, vars)

    def id_(self):
        is_array_elem = self.prev.class_ != Class.TYPE
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        if self.curr.class_ == Class.LPAREN and self.is_func_call():
            self.eat(Class.LPAREN)
            args = self.args()
            self.eat(Class.RPAREN)
            return FuncProcCall(id_, args)
        elif self.curr.class_ == Class.LBRACKET and is_array_elem:
            self.eat(Class.LBRACKET)
            index = self.logic()
            self.eat(Class.RBRACKET)
            id_ = ArrayElem(id_, index)
        if self.curr.class_ == Class.ASSIGN:
            self.eat(Class.ASSIGN)
            logic = self.logic()
            return Assign(id_, logic)
        else:
            return id_

    def idDefines(self):
        is_array_elem = self.prev.class_ != Class.TYPE
        id_ = Id(self.curr.lexeme)
        self.eat(Class.ID)
        return id_

    def if_(self):
        self.eat(Class.IF)
        cond = self.logic()
        self.eat(Class.THEN)
        self.eat(Class.BEGIN)
        true = self.block()
        self.eat(Class.END)
        false = None
        if self.curr.class_ == Class.ELSE:
            self.eat(Class.ELSE)
            if (self.curr.class_ == Class.IF):
                self.eat(Class.IF)
                cond2 = self.logic()
                self.eat(Class.THEN)
                self.eat(Class.BEGIN)
                block2 = self.block()
                self.eat(Class.END)
                self.eat(Class.ELSE)
                self.eat(Class.IF)
                cond3 = self.logic()
                self.eat(Class.THEN)
                self.eat(Class.BEGIN)
                block3 = self.block()
                self.eat(Class.END)

            else:
                self.eat(Class.BEGIN)
                false = self.block()
                self.eat(Class.END)
        self.eat(Class.SEMICOLON)
        return If(cond, true, false)

    def while_(self): 
        self.eat(Class.WHILE)
        cond = self.logic()
        self.eat(Class.DO)
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        if (self.curr.class_ == Class.SEMICOLON):
            self.eat(Class.SEMICOLON)
        return While(cond, block)

    def for_(self):
        self.eat(Class.FOR)
        init = self.id_()
        where = 'to'
        if self.curr.class_ == Class.TO:
            self.eat(Class.TO)
            where = 'to'
        elif self.curr.class_ == Class.DOWNTO:
            self.eat(Class.DOWNTO)
            where = 'downto'
        logic = self.logic()
        self.eat(Class.DO)
        self.eat(Class.BEGIN)
        block = self.block()
        self.eat(Class.END)
        self.eat(Class.SEMICOLON)
        return For(init, logic, block, Where(where))

    def repeat(self):
        self.eat(Class.REPEAT)
        block = self.block()
        self.eat(Class.UNTIL)
        cond = self.logic()
        self.eat(Class.SEMICOLON)
        return RepeatUntil(cond, block)

    def block(self):
        nodes = []
        while self.curr.class_ != Class.END:
            if self.curr.class_ == Class.VAR:
                self.eat(Class.VAR)
                nodes.append(self.variables())
                ###
            elif self.curr.class_ == Class.FUNCTION:
                nodes.append(self.func())
            ###
            elif self.curr.class_ == Class.IF:
                nodes.append(self.if_())
            elif self.curr.class_ == Class.WHILE:
                nodes.append(self.while_())
            elif self.curr.class_ == Class.FOR:
                nodes.append(self.for_())
            elif self.curr.class_ == Class.BREAK:
                nodes.append(self.break_())
            elif self.curr.class_ == Class.CONTINUE:
                nodes.append(self.continue_())
            elif self.curr.class_ == Class.EXIT:
                nodes.append(self.exit_())
            elif self.curr.class_ == Class.REPEAT:
                nodes.append(self.repeat())
            elif self.curr.class_ == Class.ID:
                nodes.append(self.id_())
                self.eat(Class.SEMICOLON)
            elif self.curr.class_ == Class.UNTIL:
                break
            else:
                self.die_deriv(self.block.__name__)
        return Block(nodes)

    def params(self):
        params = []
        while self.curr.class_ != Class.RPAREN:
            params.append(self.variables)

        return Params(params)

    def args(self):
        args = []
        while self.curr.class_ != Class.RPAREN:
            if len(args) > 0:
                self.eat(Class.COMMA)
            logic = self.logic()

            if (self.curr.class_ == Class.COLON):
                self.eat(Class.COLON)
                left = self.expr()
                self.eat(Class.COLON)
                right = self.expr()
                args.append(FormattedArg(logic, left, right))
            else:
                args.append(logic)

        return Args(args);

    def elems(self):
        elems = []
        while self.curr.class_ != Class.RPAREN:
            if len(elems) > 0:
                self.eat(Class.COMMA)
            elems.append(self.logic())
        return Elems(elems)

    def arrayElems(self, low):
        elems = []
        ctr = 0
        while self.curr.class_ != Class.RBRACE:
            if len(elems) > 0:
                self.eat(Class.COMMA)
            elems.append(ArrayElem(self.logic(), ctr + low))
            ctr += 1
        self.eat(Class.RBRACE)
        return Elems(elems)

    def break_(self):
        self.eat(Class.BREAK)
        self.eat(Class.SEMICOLON)
        return Break()

    def exit_(self):
        self.eat(Class.EXIT)
        value = None
        if self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            value = self.logic()
            self.eat(Class.RPAREN)
        self.eat(Class.SEMICOLON)

        return Exit(value)

    def continue_(self):
        self.eat(Class.CONTINUE)
        self.eat(Class.SEMICOLON)
        return Continue()

    def type_(self):
        if (self.curr.lexeme == 'string'):
            tip = self.curr.lexeme
            self.eat(Class.TYPE)
            if (self.curr.class_ == Class.LBRACKET):
                self.eat(Class.LBRACKET)
                size = self.expr()
                self.eat(Class.RBRACKET)
                type_ = TypeString(tip, size)
            else:
                type_ = TypeString(tip, None)
        else:
            type_ = Type(self.curr.lexeme)
            self.eat(Class.TYPE)
        return type_

    def factor(self):
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
        elif self.curr.class_ == Class.TRUE:
            self.eat(Class.TRUE)
            return BoolValue('true')
        elif self.curr.class_ == Class.FALSE:
            self.eat(Class.FALSE)
            return BoolValue('false')
        elif self.curr.class_ in [Class.MINUS, Class.NOT]:
            op = self.curr
            self.eat(self.curr.class_)
            first = None
            if self.curr.class_ == Class.LPAREN:
                self.eat(Class.LPAREN)
                first = self.logic()
                self.eat(Class.RPAREN)
            else:
                first = self.factor()
            return UnOp(op.lexeme, first)
        elif self.curr.class_ == Class.LPAREN:
            self.eat(Class.LPAREN)
            first = self.logic()
            self.eat(Class.RPAREN)
            return first
        elif self.curr.class_ == Class.SEMICOLON:
            return None
        else:
            self.die_deriv(self.factor.__name__)

    def term(self):
        first = self.factor()
        while self.curr.class_ in [Class.STAR, Class.FWDSLASH, Class.PERCENT, Class.MOD, Class.DIV]:
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
            elif self.curr.class_ == Class.PERCENT:
                op = self.curr.lexeme
                self.eat(Class.PERCENT)
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

        return first

    def expr(self):
        first = self.term()
        while self.curr.class_ in [Class.PLUS, Class.MINUS]:
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
        return first

    def compare(self):
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

    def logic(self):
        first = self.compare()
        if self.curr.class_ == Class.AND:
            op = self.curr.lexeme
            self.eat(Class.AND)
            second = self.compare()
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.OR:
            op = self.curr.lexeme
            self.eat(Class.OR)
            second = self.compare()
            if (self.curr.class_ == Class.AND):
                op2 = self.curr.lexeme
                self.eat(Class.AND)
                third = self.compare()
                return BinOp(op2, BinOp(op, first, second), third)
            return BinOp(op, first, second)
        elif self.curr.class_ == Class.XOR:
            op = self.curr.lexeme
            self.eat(Class.XOR)
            second = self.compare()
            return BinOp(op, first, second)
        else:
            return first

    @restorable
    def is_func_call(self):
        try:
            self.eat(Class.LPAREN)
            self.args()
            self.eat(Class.RPAREN)
            if self.curr.class_ == Class.SEMICOLON:
                self.eat(Class.SEMICOLON)
                return self.curr.class_ != Class.BEGIN
            else:
                return True

        except:
            return True

    def parse(self):
        return self.program()

    def die(self, text):
        raise SystemExit(text)

    def die_deriv(self, fun):
        self.die(f"Derivation error: {fun} {self.curr} (row:{self.curr.row}, col:{self.curr.col})")

    def die_type(self, expected, found):
        self.die(f"Expected: {expected}, Found: {found} (row:{self.curr.row}, col:{self.curr.col})")
