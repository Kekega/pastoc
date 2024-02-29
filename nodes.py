class Node():
    # Базовый класс для всех узлов абстрактного синтаксического дерева (AST).
    pass


class Program(Node):
    # Класс, представляющий узел программы в AST. Содержит список дочерних узлов (nodes).
    def __init__(self, nodes):
        self.nodes = nodes


class Decl(Node):
    # Класс для узла объявления переменной с типом (Decl). 
    # Содержит информацию о типе и идентификаторе.
    def __init__(self, type_, id_):
        self.type_ = type_
        self.id_ = id_


class ArrayDecl(Node):
    # Класс для узла объявления массива (ArrayDecl). 
    # Содержит информацию о типе, идентификаторе, границах и элементах массива.
    def __init__(self, type_, id_, low, high, elems):
        self.type_ = type_
        self.id_ = id_
        self.low = low
        self.high = high
        self.elems = elems
        self.size = high.value - low.value + 1



class ArrayElem(Node):
    # Класс для узла доступа к элементу массива (ArrayElem).
    # Содержит идентификатор массива и выражение-индекс.
    def __init__(self, id_, index):
        self.id_ = id_
        self.index = index


class Assign(Node):
    # Класс для узла присваивания (Assign). 
    # Содержит идентификатор (id_) и выражение (expr).
    def __init__(self, id_, expr):
        self.id_ = id_
        self.expr = expr


class If(Node):
    # Класс для узла условного оператора (If). 
    # Содержит условие (cond) и блоки для ветвей истинного и ложного условий.
    def __init__(self, cond, true, false):
        self.cond = cond
        self.true = true
        self.false = false


class While(Node):
    # Класс для узла цикла while (While). 
    # Содержит условие (cond) и блок, который выполняется, пока условие истинно.
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class For(Node):
    # Класс для узла цикла for (For).
    # Содержит инициализацию (init), условие (cond), блок и дополнительное условие where.
    def __init__(self, init, cond, block, where):
        self.init = init
        self.cond = cond
        self.block = block
        self.where = where


class RepeatUntil(Node):
    # Класс для узла цикла repeat-until (RepeatUntil).
    # Содержит условие (cond) и блок, который выполняется до тех пор, пока условие ложно.
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block


class FuncImpl(Node):
    # Класс для узла определения функции (FuncImpl).
    # Содержит информацию о типе возвращаемого значения, идентификаторе, параметрах, блоке и переменных.
    def __init__(self, type_, id_, params, block, var):
        self.type_ = type_
        self.id_ = id_
        self.params = params
        self.block = block
        self.var = var


class FuncProcCall(Node):
    # Класс для узла вызова функции или процедуры (FuncProcCall).
    # Содержит идентификатор и аргументы.

    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args


class ProcImpl(Node):
    # Класс для узла определения процедуры (ProcImpl).
    # Содержит информацию об идентификаторе, параметрах, блоке и переменных.
    def __init__(self, id_, params, block, var):
        self.id_ = id_
        self.params = params
        self.block = block
        self.var = var


class Block(Node):
    # Класс для узла блока кода (Block).
    # Содержит список дочерних узлов (nodes).
    def __init__(self, nodes):
        self.nodes = nodes


class Params(Node):
    # Класс для узла параметров функции или процедуры (Params).
    # Содержит список параметров.
    def __init__(self, params):
        self.params = params


class Variables(Node):
    # Класс для узла переменных (Variables).
    # Содержит список переменных.
    def __init__(self, vars):
        self.vars = vars


class Args(Node):
    # Класс для узла аргументов при вызове функции или процедуры (Args).
    # Содержит список аргументов.
    def __init__(self, args):
        self.args = args


class Elems(Node):
    # Класс для узла элементов массива (Elems).
    # Содержит список элементов.
    def __init__(self, elems):
        self.elems = elems


class Break(Node):
    pass


class Continue(Node):
    pass


class Exit(Node):
    def __init__(self, value):
        self.value = value


class Type(Node):
    # Класс для узла типа данных (Type).
    # Содержит значение типа данных.
    def __init__(self, value):
        self.value = value


class Int(Node):
    def __init__(self, value):
        self.value = value


class Char(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Real(Node):
    def __init__(self, value):
        self.value = value


class Boolean(Node):
    def __init__(self, value):
        self.value = value


class Id(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Node):
    def __init__(self, symbol, first, second):
        self.symbol = symbol
        self.first = first
        self.second = second


class UnOp(Node):
    def __init__(self, symbol, first):
        self.symbol = symbol
        self.first = first


class Where(Node):
    def __init__(self, str):
        self.value = str


class BoolValue(Node):
    def __init__(self, str):
        self.value = str


class FormattedArg(Node):
    def __init__(self, args, left, right):
        self.args = args
        self.left = left
        self.right = right


class Processor():
    # Класс для обхода дерева. 
    # Предоставляет метод visit для каждого типа узла.
    def process(self, parent, node):
        method = 'process_' + type(node).__name__
        processor = getattr(self, method, self.die)
        return processor(parent, node)

    def die(self, parent, node):
    # Обработчик ошибки для случая отсутствия метода visit для конкретного типа узла.
        method = 'process_' + type(node).__name__
        raise ValueError("Missing method: {}".format(method))
