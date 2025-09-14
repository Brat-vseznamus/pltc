from typing import List, Dict

from logic.expr import Expr

Context = List[Expr]

def context_nested(a: Context, b: Context) -> bool:
    b_repr: Dict[str, bool] = dict()

    for e in b:
        b_repr[str(e)] = True
    
    for e in a:
        if str(e) not in b_repr:
            return False
    
    return True

def context_equals(a: Context, b: Context) -> bool:
    return context_nested(a, b) and context_nested(b, a)