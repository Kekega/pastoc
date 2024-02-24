from dataclasses import dataclass

from nodes import *


@dataclass
class ElemVar:
    id : str
    type : str
    scope : str
    limit : int = 0
    counter_used : int = 0
    # params : list = []

@dataclass
class FuncVar:
    id : str
    type : str
    scope : str
    params : list


safe_funcs = [
    'read',
    'readln',
    'write',
    'writeln'
]

dec_type_assosiations = {
    'real' : 'integer',
    'string': 'char'
}

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {
        }  # Таблица символов для отслеживания объявленных переменных и их типов

        self.scopes_table = {
        }

        self.func_table = {
            'ord' : [
                FuncVar('ord', 'integer', '_', ['integer']),
                FuncVar('ord', 'integer', '_', ['char']),
                FuncVar('ord', 'integer', '_', ['boolean']),
                ],
            'chr' : [
                FuncVar('chr', 'char', '_', ['integer'])
            ]
        }

        self.scope_stack = []

    def analyze(self, node):
        if isinstance(node, Program):
            self.scope_stack.append('_')
            self.scopes_table['_'] = []
            for subnode in node.nodes:
                self.analyze(subnode)
            
            for var, l_dec in self.symbol_table.items():
                if l_dec and l_dec[-1].counter_used == 0:
                    raise Exception(f"Unused variable {var}")
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
        elif isinstance(node, ArrayDecl):
            var_id = node.id_.value
            var_type = node.type_.value
            var_limit = node.size

            scope = self.scope_stack[-1]
            elem = ElemVar(var_id, var_type, scope, var_limit)

            self.scopes_table[scope].append(elem)

            if not self.symbol_table.get(var_id):
                self.symbol_table[var_id] = []

            self.symbol_table[var_id].append(elem)
        elif isinstance(node, Assign):
            # Проверка, что переменная была объявлена
            if isinstance(node.id_, ArrayElem):
                var_id = node.id_.id_.value
            else:
                var_id = node.id_.value

            if var_id not in self.symbol_table:
                raise ValueError(f"Variable '{var_id}' is used without declaration.")

            self.symbol_table[var_id][-1].counter_used += 1

            # Проверка соответствие типов при присваивании
            assigned_type = self.get_expression_type(node.expr)
            declared_type = self.symbol_table[var_id][-1].type
            if assigned_type != declared_type and dec_type_assosiations.get(declared_type, '-') != assigned_type:
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
                # print(subnode)
                self.analyze(subnode)

        elif isinstance(node, For):
            self.analyze(node.init)
            if self.symbol_table[node.init.id_.value][-1].type != 'integer':
                raise ValueError("Expected integer type in 'For' loop assignment")
            
            # print(type(node.cond))
            if isinstance(node.cond, Int):
                pass
            elif isinstance(node.cond, Int):
                if self.symbol_table[node.cond.value][-1].type != 'integer':
                    raise ValueError("Expected integer type in 'For' loop condition")
            for subnode in node.block.nodes:
                self.analyze(subnode)
        elif isinstance(node, FuncProcCall):
            if node.id_.value in safe_funcs:
                if node.id_.value in ['read', 'readln']:
                    for a in node.args.args:
                        if isinstance(a, ArrayElem):
                            self.symbol_table[a.id_.value][-1].counter_used += 1
                        elif isinstance(a, Id):
                            self.symbol_table[a.value][-1].counter_used += 1
                        else:
                            pass

                return None
            else:
                for a in node.args.args:
                    if isinstance(a, ArrayElem):
                        self.symbol_table[a.id_.value][-1].counter_used += 1
                    elif isinstance(a, Id):
                        self.symbol_table[a.value][-1].counter_used += 1
                    # elif isinstance(a, BinOp):
                    else:
                        self.analyze(a)
                        # print(type(a))
                        # pass
    

            
                return self.func_table[self.scope_stack[-1]][-1].type # (node.id_.value)
                # raise Exception(f"Not implemented {type(node)}")
        elif isinstance(node, FuncImpl):
            if not self.func_table.get(self.scope_stack[-1]):
                self.func_table[self.scope_stack[-1]] = []
            

            # for p in node.params.params:
            #     print(p.type_.value)
            params_list = [p.type_.value for p in node.params.params]
            
            new_func = FuncVar(
                node.id_.value, 
                node.type_.value, 
                self.scope_stack[-1],
                params_list
            )
            
            # self.func_table[self.scope_stack[-1]].append(new_func)
            self.scopes_table[self.scope_stack[-1]].append(new_func)

            if not self.func_table.get(node.id_.value):
                self.func_table[node.id_.value] = []
            self.func_table[node.id_.value].append(new_func)

            # добавили функцию для вызова в предыдущий scope. Теперь работаем с новым

            self.scope_stack.append(node.id_.value)

            
            # Вызов самой себя (для рекуксии)
            new_func = FuncVar(
                node.id_.value, 
                node.type_.value, 
                self.scope_stack[-1],
                params_list
            )

            self.func_table[node.id_.value].append(new_func)

            f_var = ElemVar(node.id_.value, node.type_.value, self.scope_stack[-1]) 

            self.scopes_table[node.id_.value] = [f_var, new_func]
            self.symbol_table[node.id_.value] = [f_var]
            # print(self.scope_stack)

            # Добавим параметры функции в её scope

            for var_decl in node.params.params:
                self.analyze(var_decl)

            self.analyze(node.var)
            self.analyze(node.block)

            # pop
            # print("CLEANING", node.id_.value)
            for elem in self.scopes_table[node.id_.value]:
                # print("DELETING", elem)
                if isinstance(elem, ElemVar):
                    self.symbol_table[elem.id].pop()
                elif isinstance(elem, FuncVar):
                    self.func_table[elem.id].pop()
                else:
                    raise Exception(f"{elem}, {type(elem)}")
            
            del self.scopes_table[node.id_.value]

            self.scope_stack.pop()
        
        elif isinstance(node, ProcImpl):
            if not self.func_table.get(self.scope_stack[-1]):
                self.func_table[self.scope_stack[-1]] = []
            

            # for p in node.params.params:
            #     print(p.type_.value)
            params_list = [p.type_.value for p in node.params.params]
            
            new_func = FuncVar(
                node.id_.value, 
                "None", 
                self.scope_stack[-1],
                params_list
            )
            
            self.scopes_table[self.scope_stack[-1]].append(new_func)

            if not self.func_table.get(node.id_.value):
                self.func_table[node.id_.value] = []
            self.func_table[node.id_.value].append(new_func)

            # добавили функцию для вызова в предыдущий scope. Теперь работаем с новым

            self.scope_stack.append(node.id_.value)

            
            # Вызов самой себя (для рекуксии)
            new_func = FuncVar(
                node.id_.value, 
                "None", 
                self.scope_stack[-1],
                params_list
            )

            self.func_table[node.id_.value].append(new_func)

            self.scopes_table[node.id_.value] = [new_func]
            # self.symbol_table[node.id_.value] = []
            # print(self.scope_stack)

            # Добавим параметры функции в её scope

            for var_decl in node.params.params:
                self.analyze(var_decl)

            self.analyze(node.var)
            self.analyze(node.block)

            # for # pop
            # print("CLEANING", node.id_.value)

            for elem in self.scopes_table[node.id_.value]:
                # print("DELETING", elem)
                if isinstance(elem, ElemVar):
                    if self.symbol_table[elem.id][-1].counter_used == 0:
                        raise Exception(f"Unused variable {elem.id}. Scope {self.scope_stack[-1]}")
                    self.symbol_table[elem.id].pop()
                elif isinstance(elem, FuncVar):
                    self.func_table[elem.id].pop()
                else:
                    raise Exception(f"{elem}, {type(elem)}")
            
            del self.scopes_table[node.id_.value]

            self.scope_stack.pop()
        elif isinstance(node, RepeatUntil):
            self.analyze(node.block)
            ct = self.get_expression_type(node.cond)
            assert(ct == 'boolean')
        elif isinstance(node, Int):
            return 'integer'
        elif isinstance(node, Char):
            return 'char'
        elif isinstance(node, String):
            return 'string'
        elif isinstance(node, Char):
            return 'char'
        elif isinstance(node, Boolean):
            return 'boolean'
        else:
            raise Exception(f"Not implemented {type(node)}.") #return True

    def process_bin_op(self, node) -> str:
        numeric = ['integer', 'real']
        st = ['string', 'char']
        boole = ['boolean']
        assert isinstance(node, BinOp)
        # print(node.symbol, node.first, node.second)
        # if node.symbol in ['==']:

        if node.symbol in ['<', '>', '<=', '>=', '<>', '=']:
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
            return 'boolean'

        elif node.symbol in ['+', '-', '*', '/']:
            # only numeric types allowed
            first_type = self.get_expression_type(node.first)
            second_type = self.get_expression_type(node.second)
            if first_type not in ['integer', 'real']:
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only numeric types allowed, found '{first_type}'.")
            if second_type not in ['integer', 'real']:
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only numeric types allowed, found '{second_type}'.")
            return 'integer'
        
        elif node.symbol in ['div', 'mod']:
            first_type = self.get_expression_type(node.first)
            second_type = self.get_expression_type(node.second)
            if first_type != 'integer':
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only integer types allowed, found '{first_type}'.")
            if second_type != 'integer':
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only integer types allowed, found '{second_type}'.")
            return 'integer'
        
        elif node.symbol in ['and', 'or']:
            first_type = self.get_expression_type(node.first)
            second_type = self.get_expression_type(node.second)
            if first_type != 'boolean':
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only boolean types allowed, found '{first_type}'.")
            if second_type != 'boolean':
                raise ValueError(f"Type mismatch in '{node.symbol}'. Only boolean types allowed, found '{second_type}'.")
            return 'boolean'

        raise ValueError(f"Not implemented {node.symbol}")
        # return 'boolean'

    def get_expression_type(self, expr):
        if isinstance(expr, FuncProcCall):
            if expr.id_.value not in self.func_table:
                raise ValueError(f"Func or Proc '{expr.id_.value}' is used without declaration.")
            
            for a in expr.args.args:
                if isinstance(a, ArrayElem):
                    self.symbol_table[a.id_.value][-1].counter_used += 1
                elif isinstance(a, Id):
                    self.symbol_table[a.value][-1].counter_used += 1
                else:
                    pass
            
            # Проверка количества аргументов функции
            sc = self.func_table[expr.id_.value][-1].scope

            for i in range(len(self.func_table[expr.id_.value])):
                if self.func_table[expr.id_.value][-i - 1].scope != sc:
                    break
                try:
                    assert len(expr.args.args) == len(self.func_table[expr.id_.value][-i -1].params), f"Invalid parameter amount to {expr.id_.value}"

                    # Проверка типов переданных аргументов
                    for a, p in zip(expr.args.args, self.func_table[expr.id_.value][-i-1].params):
                        if isinstance(a, BinOp):
                            res = self.process_bin_op(a)
                            assert(res == p), f"Type missmatch in {expr.id_.value} call, {res} and {p}"
                            break
                        elif isinstance(a, Char):
                            assert('char' == p), f"Type missmatch in {expr.id_.value} call, char and {p}"
                            break
                        elif isinstance(a, Int):
                            assert('integer' == p), f"Type missmatch in {expr.id_.value} call"
                            break
                        elif isinstance(a, Boolean):
                            assert('boolean' == p), f"Type missmatch in {expr.id_.value} call"
                            break
                        elif isinstance(a, String):
                            assert('string' == p), f"Type missmatch in {expr.id_.value} call"
                            break
                        elif isinstance(a, Real):
                            assert('real' == p), f"Type missmatch in {expr.id_.value} call"
                            break
                        else:
                            assert(self.symbol_table[a.value][-1].type == p), f"Type missmatch in {expr.id_.value} call"
                            break

                    return self.func_table[expr.id_.value][-1].type
                except Exception:
                    continue
            
            assert len(expr.args.args) == len(self.func_table[expr.id_.value][-1].params), f"Invalid parameter amount to {expr.id_.value}"

            # Проверка типов переданных аргументов
            for a, p in zip(expr.args.args, self.func_table[expr.id_.value][-1].params):
                if isinstance(a, BinOp):
                    res = self.process_bin_op(a)
                    assert(res == p), f"Type missmatch in {expr.id_.value} call, {res} and {p}"
                    break
                elif isinstance(a, Char):
                    assert('char' == p), f"Type missmatch in {expr.id_.value} call, char and {p}"
                    break
                elif isinstance(a, Int):
                    assert('integer' == p), f"Type missmatch in {expr.id_.value} call"
                    break
                elif isinstance(a, Boolean):
                    assert('boolean' == p), f"Type missmatch in {expr.id_.value} call"
                    break
                elif isinstance(a, String):
                    assert('string' == p), f"Type missmatch in {expr.id_.value} call"
                    break
                elif isinstance(a, Real):
                    assert('real' == p), f"Type missmatch in {expr.id_.value} call"
                    break
                else:
                    # print(a, p)
                    assert(self.symbol_table[a.value][-1].type == p), f"Type missmatch in {expr.id_.value} call"
                    break

            return self.func_table[expr.id_.value][-1].type


        if isinstance(expr, Id):
            # Получите тип переменной из таблицы символов
            var_id = expr.value

            if var_id not in self.symbol_table:
                raise ValueError(f"Variable '{var_id}' is used without declaration.")
            self.symbol_table[var_id][-1].counter_used += 1
            return self.symbol_table[var_id][-1].type
        if isinstance(expr, ArrayElem):
            return self.symbol_table[expr.id_.value][-1].type
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
