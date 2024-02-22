from dataclasses import dataclass

from nodes import *


@dataclass
class ElemVar:
    id : str
    type : str
    scope : str

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {
        }  # Таблица символов для отслеживания объявленных переменных и их типов

        self.scopes_table = {
        }

        self.scope_stack = []

    def analyze(self, node):
        # print(self.symbol_table, self.scopes_table, self.scope_stack, sep=' | ')
        # print(node)
        if isinstance(node, Program):
            self.scope_stack.append('_')
            self.scopes_table['_'] = []
            for subnode in node.nodes:
                self.analyze(subnode)
        elif isinstance(node, Variables):
            for var_decl in node.vars:
                self.analyze(var_decl)
        elif isinstance(node, Decl):
            # Добавление переменной в таблицу символов
            var_id = node.id_.value
            var_type = node.type_.value

            scope = self.scope_stack[-1]
            elem = ElemVar(var_id, var_type, scope)

            self.scopes_table[scope].append(elem)

            if not self.symbol_table.get(var_id):
                self.symbol_table[var_id] = []

            self.symbol_table[var_id].append(elem)
            # self.symbol_table[var_id] = var_type
        elif isinstance(node, Assign):
            # Проверка, что переменная была объявлена
            print('assign')
            var_id = node.id_.value
            if var_id not in self.symbol_table:
                raise ValueError(f"Variable '{var_id}' is used without declaration.")

            # Проверка соответствие типов при присваивании
            assigned_type = self.get_expression_type(node.expr)
            declared_type = self.symbol_table[var_id][-1].type
            if assigned_type != declared_type:
                raise ValueError(f"Type mismatch in assignment for variable '{var_id}'. Expected '{declared_type}', found '{assigned_type}'.")
        elif isinstance(node, BinOp):
            # соответствие типов при бинарной операции
            self.process_bin_op(node)
        elif isinstance(node, If):
            # соответствие типов в условии
            condition_type = self.get_expression_type(node.cond)
            if condition_type != 'boolean':
                raise ValueError(f"Type mismatch in if statement condition. Expected 'boolean', found '{condition_type}'.")
            self.analyze(node.true)
            if node.false:
                self.analyze(node.false)

        elif isinstance(node, Block):
            for subnode in node.nodes:
                self.analyze(subnode)
        else:
            return True

    def process_bin_op(self, node) -> str:
        numeric = ['integer', 'real']
        st = ['string', 'char']
        boole = ['boolean']
        assert isinstance(node, BinOp)
        print(node.symbol, node.first, node.second)
        # if node.symbol in ['==']:

        if node.symbol in ['<', '>', '<=', '>=', '<>', '==']:
            first_type = self.get_expression_type(node.first)
            second_type = self.get_expression_type(node.second)  
                
            if first_type in numeric:
                first_type = numeric[0]
            elif first_type in st:
                first_type = st[0]
            elif first_type in boole:
                first_type = boole[0]

            if second_type in numeric:
                second_type = numeric[0]
            elif second_type in st:
                second_type = st[0]
            elif second_type in boole:
                second_type = boole[0]

            if first_type != second_type:
                raise ValueError(f"Type mismatch in '{node.symbol}'. Found '{self.get_expression_type(node.first)}' and '{self.get_expression_type(node.second)}'.")

        elif node.symbol in ['+', '-', '*', '/']:
            # only numeric types allowed
            first_type = self.get_expression_type(node.first)
            second_type = self.get_expression_type(node.second)
            if first_type not in ['integer', 'real']:
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only numeric types allowed, found '{first_type}'.")
            if second_type not in ['integer', 'real']:
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only numeric types allowed, found '{second_type}'.")
        
        elif node.symbol in ['div', 'mod']:
            first_type = self.get_expression_type(node.first)
            second_type = self.get_expression_type(node.second)
            if first_type != 'integer':
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only integer types allowed, found '{first_type}'.")
            if second_type != 'integer':
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only integer types allowed, found '{second_type}'.")

        return 'boolean'

    def get_expression_type(self, expr):
        if isinstance(expr, Id):
            # Получите тип переменной из таблицы символов
            var_id = expr.value
            if var_id not in self.symbol_table:
                raise ValueError(f"Variable '{var_id}' is used without declaration.")
            return self.symbol_table[var_id][-1].type
        elif isinstance(expr, Int):
            return 'integer'
        elif isinstance(expr, Real):
            return 'real'
        elif isinstance(expr, String):
            return 'string'
        elif isinstance(expr, Char):
            return 'char'
        elif isinstance(expr, BoolValue):
            return 'boolean'
        elif isinstance(expr, UnOp):
            return self.get_expression_type(expr.first)
        elif isinstance(expr, BinOp):
            return self.process_bin_op(expr)
