import re
import uuid

from nodes import *


class Generator(Processor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0
        self.lookup_table = {}
    
    var_table = []
    scope_stack = []

    nested_funcs = {}

    code_store = []
    ready_code = []

    processing = ""

    def append(self, text):
        if len(self.scope_stack) < 2:
            self.py += str(text)
            return
        self.code_store[-1] += str(text)
        

    def addtoStart(self, text):
        self.py = text + '\n' + self.py

    def newline(self):
        self.append('\n')

    def process_Program(self, parent, node):
        self.append('int main() {')
        self.newline()
        for n in node.nodes:
            if isinstance(n, Variables):
                self.process(node, n)
            if isinstance(n, Block):
                self.process(node, n)

        self.newline()
        self.append('}')
        self.newline()

        for n in node.nodes:
            if isinstance(n, ProcImpl):
                self.process(node, n)
            if isinstance(n, FuncImpl):
                self.process(node, n)

        print(self.nested_funcs)

    def process_Decl(self, parent, node):
        self.process(node, node.type_)
        self.process(node, node.id_)
        if (isinstance(node.type_, TypeString)):
            self.append('[100] = {0}')

    def process_ArrayDecl(self, parent, node):
        self.process(node, node.type_)

        self.process(node, node.id_)
        self.append('[')
        self.process(node, node.high)
        self.append('-')
        self.process(node, node.low)
        self.append('+1] ')
        if node.elems is not None:
            self.append(' = {')
            self.process(node, node.elems)
            self.append('}')

    def process_ArrayElem(self, parent, node):
        self.process(node, node.id_)
        self.append('[')
        self.process(node, node.index)
        self.append('-1]')

    def process_Assign(self, parent, node):
        if isinstance(node.id_, ArrayElem) or not node.id_.value in self.lookup_table:
            self.process(node, node.id_)
            self.append(' = ')
            self.process(node, node.expr)
        else:
            # print(node.id_.value, 'fddddddddddddddddd')
            self.append(self.lookup_table[node.id_.value])
            self.append(' = ')
            self.process(node, node.expr)

    def process_If(self, parent, node):
        self.append('if ')
        self.append('(')
        self.process(node, node.cond)
        self.append(')')
        self.append('{')
        self.newline()
        self.process(node, node.true)
        self.append('}')
        if node.false is not None:
            self.append('else{')
            self.newline()
            self.process(node, node.false)
            self.append('}')

    def process_While(self, parent, node):
        self.append('while ')
        self.append('(')
        self.process(node, node.cond)
        self.append(')')
        self.append('{')
        self.newline()
        self.process(node, node.block)
        self.append('}')
        self.newline()

    def process_For(self, parent, node):
        self.append('for (')
        self.process(node, node.init)
        self.append(';')
        if (node.where.value == 'to'):
            value = node.init.id_.value
            self.append(value)
            self.append('<=')
            self.process(node, node.cond)
            self.append(';')
            self.append(value)
            self.append('++){')
            self.newline()
            self.process(node, node.block)
        else:
            value = node.init.id_.value
            self.append(value)
            self.append('>=')
            self.process(node, node.cond)
            self.append(';')
            self.append(value)
            self.append('--){')
            self.newline()
            self.process(node, node.block)

        self.append('}')

    def process_RepeatUntil(self, parent, node):
        self.append('do')
        self.append('{')
        self.newline()
        self.process(node, node.block)
        self.append('}')
        self.newline()
        self.append('while (')
        if (isinstance(node.cond, BoolValue)):
            self.append(1)
        else:
            self.process(node, node.cond)
        self.append(')')
        self.newline()

    def process_FuncImpl(self, parent, node):
        assert isinstance(node, FuncImpl)
        for scope in self.scope_stack:
            self.nested_funcs[scope].append(node.id_.value)
        self.nested_funcs[node.id_.value] = []
        self.var_table.append([])
        self.scope_stack.append(node.id_.value)
        if len(self.scope_stack) >= 2:
            print(node.id_.value, self.nested_funcs, self.scope_stack, ">=2")
            self.code_store.append("")
        self.newline()
        self.process(node, node.type_)
        self.process(node, node.id_)
        self.append('(')
        self.process(node, node.params)
        self.append(')')

        if len(self.scope_stack) < 2:
            x = self.py.split('\n')
        else:
            x = self.code_store[-1].split('\n')
        self.addtoStart(x[-1] + ';')


        self.append('{')
        self.newline()

        ###
        node_type = node.type_.value
        if node_type == 'integer':
            self.append('int ')
        elif node_type == 'char':
            self.append('char ')
        elif node_type == 'real':
            self.append('float ')
        elif node_type == 'boolean':
            self.append('bool ')
        random_uuid = str(uuid.uuid4())[:4]
        var_name = f"_res{random_uuid}"
        self.var_table[-1].append((node_type, var_name))

        self.lookup_table[node.id_.value] = var_name

        self.append(var_name + ';')
        self.newline()

        self.process(node, node.var)
        self.process(node, node.block)
        self.newline()

        self.append('return ')
        self.append(self.lookup_table[node.id_.value] + ';')
        self.newline()
        
        del self.lookup_table[node.id_.value]
        self.append('}')
        if self.code_store:
            self.ready_code.append(self.code_store.pop())

        self.var_table.pop()
        self.scope_stack.pop()

            
    def vis_block(self, parent, node, id_):
        for n in node.nodes:
            self.process(node, n)
            if isinstance(n, If):
                pass
            elif isinstance(n, For):
                pass
            elif isinstance(n, While):
                pass
            else:
                self.append(';')
            self.newline()

    def process_ProcImpl(self, parent, node):
        self.newline()
        self.append('void ')
        self.process(node, node.id_)
        self.append('(')
        self.process(node, node.params)
        self.append(')')
        x = self.py.split('\n')

        self.addtoStart(x[-1] + ';\n')
        self.append('{')

        self.newline()
        self.process(node, node.var)
        self.process(node, node.block)
        self.newline()
        self.append('}')

    def process_FuncProcCall(self, parent, node):
        if node.id_.value == ('inc'):
            self.process(node, node.args)
            self.append('++')
        elif node.id_.value == ('length'):
            self.append('strlen(')
            self.process(node, node.args)
            self.append(')')
        elif node.id_.value == ('ord'):
            self.append('(int)(')
            self.process(node, node.args)
            self.append(')')
        elif node.id_.value == ('insert'):
            for i, n in enumerate(node.args.args):
                if i == 1:
                    self.process(node, n)
            self.append('[')
            for i, n in enumerate(node.args.args):
                if i == 2:
                    self.process(node, n)
            self.append('-1] = ')
            for i, n in enumerate(node.args.args):
                if i == 0:
                    self.process(node, n)
        elif node.id_.value == ('chr'):
            self.append('(char)(')
            self.process(node, node.args)
            self.append(')')
        elif node.id_.value == ('readln') or node.id_.value == ('read'):
            for i, n in enumerate(node.args.args):
                self.append('scanf(')
                if (isinstance(n, ArrayElem)):
                    type = self.ast.symbols.get(n.id_.value).type_

                    if (type == 'integer array'):
                        self.append('"%d",&')
                        self.process(node, n)
                    if (type == 'char array'):
                        self.append('"%c",&')
                        self.process(node, n)
                    if (type == 'real array'):
                        self.append('"%f",&')
                        self.process(node, n)
                    self.append(')')
                    if (i < len(node.args.args) - 1):
                        self.append(';')
                        self.newline()
                else:

                    type = self.ast.symbols.get(n.value).type_

                    if (type == 'integer'):
                        self.append('"%d",&')
                        self.append(n.value)
                    if (type == 'char'):
                        self.append('"%c",&')
                        self.append(n.value)
                    if (type == 'real'):
                        self.append('"%f",&')
                        self.append(n.value)
                    if (type == 'string'):
                        self.append('"%s",')
                        self.append(n.value)
                    self.append(')')
                    if (i < len(node.args.args) - 1):
                        self.append(';')
                        self.newline()
        elif node.id_.value == ('write') or node.id_.value == ('writeln'):
            for i, n in enumerate(node.args.args):
                self.append('printf(')
                if (isinstance(n, BinOp)):
                    self.append('"%d",')
                    self.process(node, n)
                elif (isinstance(n, Char)):
                    self.append('"')
                    self.append(n.value)
                    self.append('"')
                elif (isinstance(n, Id)):
                    type = self.ast.symbols.get(n.value).type_

                    if (type == 'integer'):
                        self.append('"%d",')
                        self.append(n.value)
                    if (type == 'char'):
                        self.append('"%c",')
                        self.append(n.value)
                    if (type == 'real'):
                        self.append('"%f",')
                        self.append(n.value)
                    if (type == 'string'):
                        self.append('"%s",')
                        self.append(n.value)
                elif (isinstance(n, Int)):
                    self.append('"%d",')
                    self.append(n.value)
                elif (isinstance(n, ArrayElem)):
                    self.append('"%d",')
                    self.process(node, n)
                elif (isinstance(n, Real)):
                    self.append('"%f",')
                    self.append(n.value)
                elif (isinstance(n, String)):
                    self.append('"')
                    self.append(n.value)
                    self.append('"')
                elif (isinstance(n, FormattedArg)):
                    self.process(node, n)
                elif (isinstance(n, FuncProcCall)):
                    if (n.id_.value == 'chr' or n.id_.value == 'ord'):
                        self.append('"%c",')
                    else:
                        type = parent.symbols.get(n.id_.value).type_
                        if type == 'integer':
                            self.append('"%d",')
                        elif type == 'real':
                            self.append('"%f",')
                        else:
                            self.append('"%c",')
                    self.process(node, n)

                self.append(')')
                if not (i == len(node.args.args) - 1) or node.id_.value == ('writeln'):
                    self.append(';')
                    self.newline()

            if node.id_.value == ('writeln'):
                self.append('printf("\\n")')
        else:
            self.processing = node.id_.value
            self.process(node, node.id_)
            self.append('(')
            self.process(node, node.args)
            self.append(')')

    def process_Block(self, parent, node):
        for n in node.nodes:
            self.process(node, n)
            if isinstance(n, If):
                pass
            elif isinstance(n, For):
                pass
            elif isinstance(n, While):
                pass
            elif isinstance(n, FuncImpl) or isinstance(n, ProcImpl):
                pass
            else:
                self.append(';')
                # pass
            self.newline()

    def process_Params(self, parent, node):
        t = 0
        for i, p in enumerate(node.params):
            t += 1
            if self.var_table:
                self.var_table[-1].append((p.type_.value, p.id_.value))
            if i > 0:
                self.append(', ')
            self.process(node, p)
        
        for i in range(len(self.var_table) - 1):
            for p in self.var_table[i]:
                if p[0] == 'real':
                    self.append(', ' * (t>0) + 'float ')
                if p[0] == 'integer':
                    self.append(', ' * (t>0) + 'int ')
                if p[0] == 'boolean':
                    self.append(', ' * (t>0) + 'bool ')
                if p[0] == 'string':
                    self.append(', ' * (t>0) + 'char[] ')
                if p[0] == 'char':
                    self.append(', ' * (t>0) + 'char ')
                self.append(f"*{p[1]}")
                t += 1

    def process_Variables(self, parent, node):
        for n in node.vars:
            if self.var_table:
                self.var_table[-1].append((n.type_.value, n.id_.value))
            self.process(node, n)
            self.append(';')
            self.newline()

    def process_Args(self, parent, node):
        # вызов функции
        t = 0
        for i, a in enumerate(node.args):
            t += 1
            if i > 0:
                self.append(', ')
            self.process(node, a)
        
        if self.scope_stack and self.processing not in self.nested_funcs[self.scope_stack[-1]]:
            return
        if self.var_table:
            for i in range(len(self.var_table)):
                for p in self.var_table[i]:
                    if i < len(self.var_table) - 1:
                        self.append(', '* (t>0) + f'{p[1]}')
                    else:
                        self.append(', '* (t>0) + f'&{p[1]}')
                    t += 1
                

    def process_Elems(self, parent, node):
        for i, e in enumerate(node.elems):
            if i > 0:
                self.append(', ')
            self.process(node, e)

    def process_TypeString(self, parent, node):
        self.append('char ')

    def process_Type(self, parent, node):
        if node.value == 'real':
            self.append('float ')
        if node.value == 'integer':
            self.append('int ')
        if node.value == 'boolean':
            self.append('int ')
        if node.value == 'string':
            self.append('char[] ')
        if node.value == 'char':
            self.append('char ')

    def process_Int(self, parent, node):
        self.append(node.value)

    def process_Char(self, parent, node):
        self.append("'" + node.value + "'")

    def process_String(self, parent, node):
        self.append(node.value)

    def process_Real(self, parent, node):
        self.append(node.value)

    def process_Boolean(self, parent, node):
        if node.value == 'true':
            self.append('1')
        else:
            self.append('0')

    def process_Id(self, parent, node):
        if self.scope_stack:
            for k in range(len(self.var_table) - 1):
                for v in self.var_table[k]:
                    if node.value == v[1]:
                        self.append('*')
                        self.append(node.value)
                        return
        self.append(node.value)

    def process_BinOp(self, parent, node):

        self.process(node, node.first)
        if node.symbol == 'mod':
            self.append(' % ')
        elif node.symbol == 'div':
            self.append(' / ')
        elif node.symbol == '/':
            self.append('/')
        elif node.symbol == 'and':
            self.append(' && ')
        elif node.symbol == '=':
            self.append(' == ')
        elif node.symbol == 'or':
            self.append(' || ')
        elif node.symbol == '<>':
            self.append(' != ')
        else:
            self.append(node.symbol)
        self.process(node, node.second)

    def process_UnOp(self, parent, node):
        if node.symbol == '-':
            self.append('-')
        elif node.symbol != '&':
            self.append(node.symbol)
        self.process(node, node.first)

    def process_Where(self, parent, node):
        pass

    def process_BoolValue(self, parent, node):
        if node.value == 'true':
            self.append('1')
        else:
            self.append('0')

    def process_FormattedArg(self, parent, node):
        self.append('"%.')
        self.process(node, node.right)
        self.append('f",')
        self.process(node, node.args)

    def format_c_code(self, input_code):
        formatted_code = ""
        tab_count = 0

        for char in input_code:
            if char == '\n':
                formatted_code += '\n' + '\t' * tab_count
            elif char == '{':
                tab_count += 1
                formatted_code += char
            elif char == '}':
                tab_count = max(0, tab_count - 1)
                formatted_code += char
            else:
                formatted_code += char

        return formatted_code

    def generate(self, path):
        self.process(None, self.ast)


        print(self.code_store)
        for code in self.ready_code:
            self.py += code

        self.py = "#include<stdio.h>\n\n\n" + self.py
        self.py = re.sub('\n\s*\n', '\n', self.py)
        self.py = self.format_c_code(self.py)
        with open(path, 'w') as source:
            source.write(self.py)
        return path
