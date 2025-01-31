# The original code that MathLamp originated was from a Lark template.
# Check it here -> https://github.com/lark-parser/lark/blob/08c91939876bd3b2e525441534df47e0fb25a4d1/examples/calc.py
from lark import Lark, Transformer, v_args

grammar = r"""
?start: sum
          | NAME "=" sum    -> assign_var

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div
        | product "%" atom  -> mod

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"
         | "out" "[" sum "]" -> out
         | "sqrt" "[" sum "]" -> sqrt
         | "pow" "[" sum "," sum "]" -> pow

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS

    %ignore WS
    %ignore /\/\/[^\n]*/
"""

out_results = []

@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, truediv as div, neg, mod, pow
    from math import sqrt
    number = float

    def __init__(self):
        super().__init__()
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("ERROR: Variable not found: %s" % name)

    def out(self, value):
        out_results.append(value)


calc_parser = Lark(grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse
