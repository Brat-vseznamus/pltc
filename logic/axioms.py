from logic.expr import Expr, V, I, O, A, N
from logic.proof_type import ProofTypeBase

from typing import List

class Axiom(ProofTypeBase):
    Axioms: List[Expr] = [
        I(V("A"), I(V("B"), V("A"))),
        I(I(V("A"), V("B")), I(I(V("A"), I(V("B"), V("C"))), I(V("A"), V("C")))),
        I(V("A"), I(V("B"), A(V("A"), V("B")))),
        I(A(V("A"), V("B")), V("A")),
        I(A(V("A"), V("B")), V("B")),
        I(V("A"), O(V("A"), V("B"))),
        I(V("B"), O(V("A"), V("B"))),
        I(I(V("A"), V("C")), I(I(V("B"), V("C")), I(O(V("A"), V("B")), V("C")))),
        I(I(V("A"), V("B")), I(I(V("A"), N(V("B"))), N(V("A")))),
        I(N(N(V("A"))), V("A"))
    ]

    def __init__(self, index: int):
        self.index = index
    
    def __str__(self):
        return f"Ax.{self.index}"
    
    def fit_expr(self, e: Expr) -> bool:
        if not(0 <= self.index < len(self.Axioms)):
            return False
        return e.fit_template(self.Axioms[self.index])
