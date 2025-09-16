from typing import List, Dict, Union, Tuple, Optional
from enum import Enum

def expr(input: str) -> "Expr":
    """
    Generator of expressions or raise `TypeError`
    """
    result = parse_expr(input)
    if isinstance(result, ParsingError):
        raise TypeError(result)
    return result

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


# parsing error
class ParsingError:
    def __init__(self, position: int, message: str):
        self.position = position
        self.message = message

Letters = [chr(x) for x in range(ord("A"), ord("Z") + 1)]

class Operator(Enum):
    LEFT_BRACKET = "("
    RIGHT_BRACKET = ")"
    NEGATION = "!"
    AND = "&"
    OR = "|"
    IMPLICATION = "->"

    def priority(self) -> Optional[int]:
        if self == Operator.LEFT_BRACKET:
            return 1
        if self == Operator.RIGHT_BRACKET:
            return 1
        if self == Operator.NEGATION:
            return 2
        if self == Operator.AND:
            return 3
        if self == Operator.OR:
            return 4
        if self == Operator.IMPLICATION:
            return 5
        return None
    
    def is_binary(self) -> bool:
        if self == Operator.AND:
            return True
        if self == Operator.OR:
            return True
        if self == Operator.IMPLICATION:
            return True
        return False
        
    def is_right_assosiated(self) -> bool:
        if self == Operator.AND:
            return True
        if self == Operator.OR:
            return True
        if self == Operator.IMPLICATION:
            return False
        return False
    
    def to_expression(self, children: List[Expr]) -> Optional[Expr]:
        if self == Operator.NEGATION and len(children) == 1:
            return Not(children[0])
        if self == Operator.AND and len(children) == 2:
            return And(children[0], children[1])
        if self == Operator.OR and len(children) == 2:
            return Or(children[0], children[1])
        if self == Operator.IMPLICATION and len(children) == 2:
            return Impl(children[0], children[1])
        return None

class Token:
    def __init__(self, value: Union[Operator, Variable], position: int):
        self.value = value
        self.position = position
    

def parse_tokens(input: str) -> Union[List[Token], ParsingError]:
    result: List[Token] = []

    left_bracket_pairs: Dict[int, int] = dict()
    left_bracket_stack: List[int] = list()

    i = 0
    while i < len(input):
        c = input[i]
        i += 1
        if c == " ":
            continue
        if c in Letters:
            result.append(Token(Variable(c), i - 1))
            continue
        if c == Operator.LEFT_BRACKET.value:
            result.append(Token(Operator.LEFT_BRACKET, i - 1))

            left_bracket_stack.append(len(result) - 1)
            continue
        if c == Operator.RIGHT_BRACKET.value:
            result.append(Token(Operator.RIGHT_BRACKET, i - 1))

            if len(left_bracket_stack) == 0:
                return ParsingError(i - 1, "no open bracket for this close bracket")
            left_index = left_bracket_stack.pop()
            left_bracket_pairs[left_index] = len(result) - 1
            continue
        if c == Operator.NEGATION.value:
            result.append(Token(Operator.NEGATION, i - 1))
            continue
        if c == Operator.OR.value:
            result.append(Token(Operator.OR, i - 1))
            continue
        if c == Operator.AND.value:
            result.append(Token(Operator.AND, i - 1))
            continue
        if c == "-":
            if i >= len(input) or input[i] != '>':
                return ParsingError(i - 1, "can't parse ->")
            else:
                i += 1
                result.append(Token(Operator.IMPLICATION, i - 2))
                continue
        else:
            return ParsingError(i - 1, f"unknown symbol \"{c}\"")
    
    if len(left_bracket_stack) != 0:
        return ParsingError(result[left_bracket_stack.pop()].position, "no close bracket for this open bracket")
    
    return result

def parse_expr(input: str) -> Union[Expr, ParsingError]:
    tokens = parse_tokens(input)
    if isinstance(tokens, ParsingError):
        return tokens
    else:
        result = _parse_layer(tokens, -1, False)
        if isinstance(result, ParsingError):
            return result
        else:
            return result[0]

# Var, (), !, &, |, ->
def _parse_layer(tokens: List[Token], last_position: int, wait_right_bracket: bool) -> Union[Tuple[Expr, List[Token]], ParsingError]:
    if len(tokens) == 0:
        return ParsingError(last_position, "no tokens to continue parsing")
    
    current_stack: List[Expr] = []
    current_operator_stack: List[Operator] = []
    
    rest = tokens

    while len(rest) > 0:
        head, rest = rest[0], rest[1:]
        if len(current_stack) == len(current_operator_stack):
            # tokens = (...) tokens
            if head.value == Operator.LEFT_BRACKET:
                
                result = _parse_layer(rest, head.position, True)
                if isinstance(result, ParsingError):
                    return result
                expr, rest = result
                current_stack.append(expr)
            # tokens = ! tokens
            elif head.value == Operator.NEGATION:
                if len(rest) == 0:
                    return ParsingError(head.position, "no value for negation")
                inner, rest = rest[0], rest[1:]
                not_count = 1
                while not isinstance(inner.value, Variable) \
                    and len(rest) != 0 \
                    and inner.value == Operator.NEGATION:

                    not_count += 1
                    inner, rest = rest[0], rest[1:]

                def wrap_inner(e: Expr) -> Expr:
                    for i in range(not_count):
                        e = Not(e)
                    return e

                # tokens = !A tokens
                if isinstance(inner.value, Variable):
                    current_stack.append(wrap_inner(inner.value))
                else:
                    # tokens = !(...) tokens
                    if inner.value == Operator.LEFT_BRACKET:
                        result = _parse_layer(rest, inner.position, True)
                        if isinstance(result, ParsingError):
                            return result
                        expr, rest = result
                        current_stack.append(wrap_inner(expr))
                    else:
                        return ParsingError(inner.position, f"unexpected symbol after negation {inner.value.value}")
            # tokens = Var tokens
            elif isinstance(head.value, Variable):
                current_stack.append(head.value)
            else:
                return ParsingError(head.position, "expected unary expression after binary operator")
        elif len(current_stack) == len(current_operator_stack) + 1:
            # tokens = & tokens
            if head.value == Operator.AND:
                current_operator_stack.append(head.value)
            # tokens = | tokens
            elif head.value == Operator.OR:
                current_operator_stack.append(head.value)
            # tokens = -> tokens
            elif head.value == Operator.IMPLICATION:
                current_operator_stack.append(head.value)
            # tokens = ) tokens
            elif head.value == Operator.RIGHT_BRACKET:
                if wait_right_bracket:
                    wait_right_bracket = False
                    break
                else:
                    return ParsingError(head.position, "unexpected close bracket")
            else:
                return ParsingError(head.position, "expected binary operator or close bracket")
        else:
            return ParsingError(head.position, "incorrect parsing state")
    
    if wait_right_bracket:
        return ParsingError(last_position, "missing expected close bracket in current level")
    
    if len(current_stack) != len(current_operator_stack) + 1:
        return ParsingError(last_position, "missing expected item for binary operator in current level")

    if len(current_operator_stack) == 0:
        return [current_stack[0], rest]

    def combine_expression(items: List[Expr], operators: List[Operator]) -> Tuple[Expr, List[Expr], List[Operator]]:
        if len(items) == 0:
            raise TypeError("impossible")
        if len(items) == 1:
            return items[0], list(), list()
        left, right = items[0], items[1]
        op = operators[0]

        rest_ops = operators[1:]
        rest_items = items[1:]

        while len(rest_ops) > 0:
            new_op = rest_ops[0]
            if new_op.priority() > op.priority():
                left = op.to_expression([left, right])
                right = rest_items[1]
                op = new_op

                rest_items = rest_items[1:]
                rest_ops = rest_ops[1:]
                
            elif new_op.priority() < op.priority():
                right, rest_items, rest_ops = combine_expression(rest_items, rest_ops)
            else:
                if op.is_right_assosiated():
                    left = op.to_expression([left, right])
                    right = rest_items[1]
                    op = new_op

                    rest_items = rest_items[1:]
                    rest_ops = rest_ops[1:]
                else:
                    right, rest_items, rest_ops = combine_expression(rest_items, rest_ops)
        
        return op.to_expression([left, right]), rest_items, rest_ops
    
    return combine_expression(current_stack, current_operator_stack)[0], rest

        
        
    

    
    
            