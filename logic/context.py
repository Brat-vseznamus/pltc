from typing import List, Dict, Optional

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

def remove_from_context(context: Context, e: Expr) -> Context:
    return [assum for assum in context if e != assum]

def context_contains_expr(context: Context, e: Expr) -> bool:
    return e in context

def add_to_context(context: Context, es: List[Expr]) -> Context:
    new_context = [assum for assum in context]
    for e in es:
        if e not in new_context:
            new_context.append(e)
    return new_context