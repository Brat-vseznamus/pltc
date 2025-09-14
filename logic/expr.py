from typing import List, Dict

class Expr:
    def __init__(self, value: str, children: List["Expr"]):
        self.value = value
        self.children = children
    
    def __eq__(self, other):
        if isinstance(other, Expr):
            if self.value != other.value:
                return False
            if len(self.children) != len(other.children):
                return False
            for i in range(len(self.children)):
                if not (self.children[i] == other.children[i]):
                    return False
            return True
        return False
    
    def __str__(self):
        if len(self.children) > 0:
            if len(self.children) == 1:
                s = self.value
                s += self.children[0].__str__()
                return s
            if len(self.children) == 2:
                s = "("
                s += self.children[0].__str__()
                s += self.value
                s += self.children[1].__str__()
                s += ")"
                return s
            return "???"
        else:
            return self.value
    
    def fit_template(self, template: "Expr") -> bool:
        return self._fit_template(template, dict())
    
    def _fit_template(self, template: "Expr", mapping: Dict[str, "Expr"]) -> bool:
        if isinstance(template, Variable):
            if template.value not in mapping:
                mapping[template.value] = self
            return mapping[template.value] == self
        else:
            if template.value != self.value:
                return False
            if len(template.children) != len(self.children):
                return False
            for i in range(len(self.children)):
                if not self.children[i]._fit_template(template.children[i], mapping):
                    return False
            return True
    
    def replace(self, mapping: Dict[str, "Expr"]) -> "Expr":
        if isinstance(self, Variable):
            if self.value not in mapping:
                return Variable(self.value)
            return mapping[self.value]
        else:
            return Expr(self.value, [c.replace(mapping) for c in self.children])

class BinExpr(Expr):
    def __init__(self, value, left, right):
        super().__init__(value, list([left, right]))

class UnaryExpr(Expr):
    def __init__(self, value, inner_expr):
        super().__init__(value, list([inner_expr]))

# zero exprs
class Variable(Expr):
    def __init__(self, value):
        super().__init__(value, list())

# unary exprs
class Not(UnaryExpr):
    def __init__(self, inner_expr):
        super().__init__("!", inner_expr)

# bin exprs
class Impl(BinExpr):
    def __init__(self, left, right):
        super().__init__("->", left, right)

class Or(BinExpr):
    def __init__(self, left, right):
        super().__init__("|", left, right)

class And(BinExpr):
    def __init__(self, left, right):
        super().__init__("&", left, right)

# type aliases
V = Variable
I = Impl
O = Or
A = And
N = Not