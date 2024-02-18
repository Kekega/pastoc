import re
import uuid

from nodes import *


class Generator(Processor):
    def __init__(self, ast):
        self.ast = ast
        self.py = ""
        self.level = 0
        self.lookup_table = {}
    

    def append(self, text):
        self.py += str(text)


    def addtoStart(self, text):
        self.py = text + '\n' + self.py

    def newline(self):
        self.append('\n')

    def visit_Program(self, parent, node):
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

        pass

    def visit_Decl(self, parent, node):
        self.process(node, node.type_)
        self.process(node, node.id_)
        if (isinstance(node.type_, TypeString)):
            self.append('[100] = {0}')

    def visit_ArrayDecl(self, parent, node):
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

    def visit_ArrayElem(self, parent, node):
        self.process(node, node.id_)
        self.append('[')
        self.process(node, node.index)
        self.append('-1]')

    def visit_Assign(self, parent, node):
        if isinstance(node.id_, ArrayElem) or not node.id_.value in self.lookup_table:
            self.process(node, node.id_)
            self.append(' = ')
            self.process(node, node.expr)
        else:
            self.append(self.lookup_table[node.id_.value])
            self.append(' = ')
            self.process(node, node.expr)

    def visit_If(self, parent, node):
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

    def visit_While(self, parent, node):
        self.append('while ')
        self.append('(')
        self.process(node, node.cond)
        self.append(')')
        self.append('{')
        self.newline()
        self.process(node, node.block)
        self.append('}')
        self.newline()

    def visit_For(self, parent, node):
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

    def visit_RepeatUntil(self, parent, node):
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

    def visit_FuncImpl(self, parent, node):
        self.newline()
        self.process(node, node.type_)
        # self.append(' ')
        self.process(node, node.id_)
        self.append('(')
        self.process(node, node.params)
        self.append(')')
        x = self.py.split('\n')

        self.addtoStart(x[-1] + ';')
        self.append('{')
        self.newline()


        # self.append(node.type_.value + ' ')


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
        random_uuid = str(uuid.uuid4())[:8]
        var_name = f"_res{random_uuid}"

        self.lookup_table[node.id_.value] = var_name

        self.append(var_name + ';')
        self.newline()

        self.process(node, node.var)
        self.process(node, node.block)
        # self.vis_block(node, node.block, node.id_)
        self.newline()

        ###

        self.append('return ')
        self.append(self.lookup_table[node.id_.value] + ';')
        self.newline()
        
        del self.lookup_table[node.id_.value]

        self.append('}')
            
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
        # self.append('return ')
        # self.append(self.assosiate_table[id_] + ';')
        
        # del self.assosiate_table[id_]

    def visit_ProcImpl(self, parent, node):
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

    def visit_FuncProcCall(self, parent, node):
        if node.id_.value == ('inc'):
            self.process(node, node.args)
            self.append('++')
        elif node.id_.value == ('length'):
            self.append('strlen(')
            self.process(node, node.args)
            self.append(')')
        elif node.id_.value == ('ord'):
            self.process(node, node.args)
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
            self.process(node, node.args)
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
                if (i < len(node.args.args) - 1) or (len(node.args.args) == 1 and node.id_.value == ('writeln')):
                    self.append(';')
                    self.newline()

            if node.id_.value == ('writeln'):
                self.append('printf("\\n")')
        else:
            self.process(node, node.id_)
            self.append('(')
            self.process(node, node.args)
            self.append(')')

    def visit_Block(self, parent, node):
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

    def visit_Params(self, parent, node):
        for i, p in enumerate(node.params):
            if i > 0:
                self.append(', ')
            self.process(node, p)

    def visit_Variables(self, parent, node):
        for n in node.vars:
            self.process(node, n)
            self.append(';')
            self.newline()

    def visit_Args(self, parent, node):
        for i, a in enumerate(node.args):
            if i > 0:
                self.append(', ')
            self.process(node, a)

    def visit_Elems(self, parent, node):
        for i, e in enumerate(node.elems):
            if i > 0:
                self.append(', ')
            self.process(node, e)

    def visit_Break(self, parent, node):
        self.append('break')

    def visit_Continue(self, parent, node):
        self.append('continue')

    def visit_Exit(self, parent, node):
        self.append('return')
        if node.value is not None:
            self.append('(')
            self.process(node, node.value)
            self.append(')')

    def visit_TypeString(self, parent, node):
        self.append('char ')

    def visit_Type(self, parent, node):
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

    def visit_Int(self, parent, node):
        self.append(node.value)

    def visit_Char(self, parent, node):
        self.append("'" + node.value + "'")

    def visit_String(self, parent, node):
        self.append(node.value)

    def visit_Real(self, parent, node):
        self.append(node.value)

    def visit_Boolean(self, parent, node):
        if node.value == 'true':
            self.append('1')
        else:
            self.append('0')

    def visit_Id(self, parent, node):
        self.append(node.value)

    def visit_BinOp(self, parent, node):

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

    def visit_UnOp(self, parent, node):
        if node.symbol == '-':
            self.append('-')
        elif node.symbol != '&':
            self.append(node.symbol)
        self.process(node, node.first)

    def visit_Where(self, parent, node):
        pass

    def visit_BoolValue(self, parent, node):
        if node.value == 'true':
            self.append('1')
        else:
            self.append('0')

    def visit_FormattedArg(self, parent, node):
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
        self.py = "#include<stdio.h>\n\n\n" + self.py
        self.py = re.sub('\n\s*\n', '\n', self.py)
        self.py = self.format_c_code(self.py)
        with open(path, 'w') as source:
            source.write(self.py)
        return path
