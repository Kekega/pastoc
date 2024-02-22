from nodes import Processor


class Symbol:
    def __init__(self, id_, type_, scope):
        self.id_ = id_
        self.type_ = type_
        self.scope = scope

    def __str__(self):
        return "<{} {} {}>".format(self.id_, self.type_, self.scope)

    def copy(self):
        return Symbol(self.id_, self.type_, self.scope)


class Symbols:
    def __init__(self):
        self.symbols = {}

    def put(self, id_, type_, scope):
        self.symbols[id_] = Symbol(id_, type_, scope)

    def get(self, id_):
        if self.symbols.get(id_) == None:
            pass
        try:
            return self.symbols[id_]
        except KeyError:
            raise ValueError(f"{id_} is not defined")

    def contains(self, id_):
        return id_ in self.symbols

    def remove(self, id_):
        del self.symbols[id_]

    def __len__(self):
        return len(self.symbols)

    def __str__(self):
        out = ""
        for _, value in self.symbols.items():
            if len(out) > 0:
                out += "\n"
            out += str(value)
        return out

    def __iter__(self):
        return iter(self.symbols.values())

    def __next__(self):
        return next(self.symbols.values())


class Symbolizer(Processor):
    def __init__(self, ast):
        self.ast = ast

    def process_Program(self, parent, node):
        node.symbols = Symbols()
        for n in node.nodes:
            self.process(node, n)

    def process_Decl(self, parent, node):
        parent.symbols.put(node.id_.value, node.type_.value, id(parent))

    def process_ArrayDecl(self, parent, node):
        node.symbols = Symbols()
        parent.symbols.put(node.id_.value, node.type_.value + ' array', id(parent))

    def process_ArrayElem(self, parent, node):
        pass

    def process_Assign(self, parent, node):
        pass

    def process_If(self, parent, node):
        node.symbols = Symbols()
        self.process(node, node.true)
        if node.false is not None:
            self.process(node, node.false)

    def process_While(self, parent, node):
        node.symbols = Symbols()
        self.process(node, node.block)

    def process_For(self, parent, node):
        node.symbols = Symbols()
        self.process(node, node.block)

    def process_RepeatUntil(self, parent, node):
        node.symbols = Symbols()
        self.process(node, node.block)

    def process_FuncImpl(self, parent, node):
        node.symbols = Symbols()
        parent.symbols.put(node.id_.value, node.type_.value, id(parent))
        node.symbols.put(node.id_.value, node.type_.value, id(parent))
        self.process(node, node.var)
        self.process(node, node.block)
        self.process(node, node.params)

    def process_ProcImpl(self, parent, node):
        node.symbols = Symbols()
        parent.symbols.put(node.id_.value, 'void', id(parent))
        node.symbols.put(node.id_.value, 'void', id(parent))
        self.process(node, node.var)
        self.process(node, node.block)
        self.process(node, node.params)

    def process_FuncProcCall(self, parent, node):
        pass

    def process_Block(self, parent, node):
        node.symbols = parent.symbols
        for n in node.nodes:
            self.process(parent, n)

    def process_Params(self, parent, node):

        for p in node.params:
            self.process(parent, p)

    def process_Variables(self, parent, node):

        for p in node.vars:
            self.process(parent, p)

    def process_Args(self, parent, node):
        pass

    def process_Elems(self, parent, node):
        pass

    def process_Break(self, parent, node):
        pass

    def process_Continue(self, parent, node):
        pass

    def process_Exit(self, parent, node):
        pass

    def process_TypeString(self, parent, node):
        pass

    def process_Type(self, parent, node):
        pass

    def process_Int(self, parent, node):
        pass

    def process_Char(self, parent, node):
        pass

    def process_String(self, parent, node):
        pass

    def process_Real(self, parent, node):
        pass

    def process_Boolean(self, parent, node):
        pass

    def process_Id(self, parent, node):
        pass

    def process_BinOp(self, parent, node):
        pass

    def process_UnOp(self, parent, node):
        pass

    def process_Where(self, parent, node):
        pass

    def process_BoolValue(self, parent, node):
        pass

    def process_FormattedArg(self, parent, node):
        pass

    def symbolize(self):
        self.process(None, self.ast)
