from code_gen import Generator
from grapher import Grapher
from lexer import Lexer
from nodes import *
from parser_pasc import Parser
from semantic import SemanticAnalyzer
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


if __name__ == "__main__":
    with open(args['src'], 'r') as source:
        text = source.read()
        lexer = Lexer(text)
        tokens = lexer.lex()
        # print(tokens)
        # print([(tok.class_, tok.lexeme) for tok in tokens])
        parser = Parser(tokens)
        ast = parser.parse()

        # for node in ast.nodes[0].params.params:
        #     print(node)

        # grapher = Grapher(ast)
        # img = grapher.graph()
        # Image(img)
        # print(ast)

        sem = SemanticAnalyzer()
        sem.analyze(ast)

        symbolizer = Symbolizer(ast)
        symbolizer.symbolize()
        generator = Generator(ast)
        generator.generate(args['gen'])
