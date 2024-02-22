from code_gen import Generator
from lexer import Lexer
from nodes import *
from parser_pasc import Parser
from symbols import *

DEBUG = True  

if DEBUG:
    test_id = '20'
    path_root = 'tests/'
    args = {}
    args['src'] = f'{path_root}{test_id}/src.pas'
    args['gen'] = f'{path_root}{test_id}/gen.c'
else:
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('src') 
    arg_parser.add_argument('gen')
    args = vars(arg_parser.parse_args())

from graphviz import Digraph, Source


class Grapher(Processor):
    def __init__(self, ast):
        self.ast = ast
        self._count = 1
        self.dot = Digraph()
        self.dot.node_attr['shape'] = 'box'
        self.dot.node_attr['height'] = '0.1'
        self.dot.edge_attr['arrowsize'] = '0.5'

    def add_node(self, parent, node, name=None):
        node._index = self._count
        self._count += 1
        caption = type(node).__name__
        if name is not None:
            caption = '{} : {}'.format(caption, name)
        self.dot.node('node{}'.format(node._index), caption)
        if parent is not None:
            self.add_edge(parent, node)

    def add_edge(self, parent, node):
        src, dest = parent._index, node._index
        self.dot.edge('node{}'.format(src), 'node{}'.format(dest))

    def visit_Program(self, parent, node):
        self.add_node(parent, node)
        for n in node.nodes:
            self.process(node, n)

    def visit_Variables(self, parent, node):
        self.add_node(parent, node)
        for n in node.vars:
            self.process(node, n)

    def visit_FuncImpl(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.type_)
        self.process(node, node.id_)
        self.process(node, node.params)
        self.process(node, node.block)
        self.process(node, node.var)

    def visit_ProcImpl(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.id_)
        self.process(node, node.params)
        self.process(node, node.block)
        self.process(node, node.var)

    def visit_Decl(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.type_)
        self.process(node, node.id_)

    def visit_ArrayDecl(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.type_)
        self.process(node, node.id_)
        self.process(node, node.low)
        self.process(node, node.high)
        if node.elems is not None:
            self.process(node, node.elems)

    def visit_RepeatUntil(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.cond)
        self.process(node, node.block)

    def visit_ArrayElem(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.id_)
        self.process(node, node.index)

    def visit_Assign(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.id_)
        self.process(node, node.expr)

    def visit_If(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.cond)
        self.process(node, node.true)
        if node.false is not None:
            self.process(node, node.false)

    def visit_While(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.cond)
        self.process(node, node.block)

    def visit_For(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.init)
        self.process(node, node.cond)
        self.process(node, node.block)
        self.process(node, node.where)

    def visit_FuncProcCall(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.id_)
        self.process(node, node.args)

    def visit_Block(self, parent, node):

        self.add_node(parent, node)
        for n in node.nodes:
            self.process(node, n)

    def visit_Params(self, parent, node):
        self.add_node(parent, node)
        for p in node.params:
            self.process(node, p)

    def visit_Args(self, parent, node):
        self.add_node(parent, node)
        for a in node.args:
            self.process(node, a)

    def visit_Elems(self, parent, node):
        self.add_node(parent, node)
        for e in node.elems:
            self.process(node, e)

    def visit_Break(self, parent, node):
        self.add_node(parent, node)

    def visit_Continue(self, parent, node):
        self.add_node(parent, node)

    def visit_Exit(self, parent, node):
        self.add_node(parent, node)
        if node.value is not None:
            self.process(node, node.value)

    def visit_Return(self, parent, node):
        self.add_node(parent, node)
        if node.expr is not None:
            self.process(node, node.expr)

    def visit_Type(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_TypeString(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)
        if node.size is not None:
            self.process(node, node.size)

    def visit_Int(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Char(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_String(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Real(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Boolean(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_Id(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_BinOp(self, parent, node):
        name = node.symbol
        self.add_node(parent, node, name)
        self.process(node, node.first)
        self.process(node, node.second)

    def visit_UnOp(self, parent, node):
        name = node.symbol
        self.add_node(parent, node, name)
        self.process(node, node.first)

    def visit_Where(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_BoolValue(self, parent, node):
        name = node.value
        self.add_node(parent, node, name)

    def visit_FormattedArg(self, parent, node):
        self.add_node(parent, node)
        self.process(node, node.args)
        self.process(node, node.left)
        self.process(node, node.right)

    def graph(self):
        self.process(None, self.ast)
        s = Source(self.dot.source, filename='graph', format='png')
        return s.view()


if __name__ == "__main__":
    with open(args['src'], 'r') as source:
        text = source.read()
        lexer = Lexer(text)
        tokens = lexer.lex()
        # print(tokens)
        print([(tok.class_, tok.lexeme) for tok in tokens])
        parser = Parser(tokens)
        ast = parser.parse()
        # print(ast)

        # for node in ast.nodes[0].params.params:
        #     print(node)

        # grapher = Grapher(ast)
        # img = grapher.graph()
        # Image(img)
        # print(ast)

        # from semantic import SemanticAnalyzer
        # sem = SemanticAnalyzer()
        # sem.analyze(ast)

        symbolizer = Symbolizer(ast)
        symbolizer.symbolize()
        generator = Generator(ast)
        generator.generate(args['gen'])
