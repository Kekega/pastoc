from code_gen import Generator
from lexer import Lexer
from nodes import *
from parser_pasc import Parser
from symbols import *

DEBUG = True  

if DEBUG:
    #10 - 13, 17

    test_id = '17' 
    path_root = 'tests/'
    args = {}
    args['src'] = f'{path_root}{test_id}/src.pas'
    args['gen'] = f'{path_root}{test_id}/gen.c'
    # args['gen'] = 'gen.c'
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
        # print([(tok.class_, tok.lexeme) for tok in tokens])
        parser = Parser(tokens)
        ast = parser.parse()
        # print(ast)
        symbolizer = Symbolizer(ast)
        symbolizer.symbolize()
        generator = Generator(ast)
        #code = generator.generate('main1.py')
        generator.generate(args['gen'])
        # runner = Runner(ast)
        # runner.run()
