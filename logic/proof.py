from typing import List, Union, Tuple, Optional

from logic.expr import Expr, Impl
from logic.axioms import Axiom
from logic.context import Context

class Assumption:
    def __init__(self, index: int):
        self.index = index
        
    def __str__(self):
        return f"Assum.{self.index}"

class MP:
    def __init__(self, index1: int, index2: int):
        self.index1 = index1
        self.index2 = index2
    
    def __str__(self):
        return f"MP {self.index1}, {self.index2}"

# class Lemma:
#     def __init__(self, proof: "Proof"):
#         self.proof = proof

ProofType = Union[Axiom, Assumption, MP]

class ProofStep:
    def __init__(self, formula: Expr, proof_type: ProofType):
        self.formula = formula
        self.proof_type = proof_type

class Proof:
    def __init__(self, context: Context, steps: List[ProofStep]):
        self.context = context
        self.steps = steps
    
    def is_correct(self) -> Tuple[bool, int]:
        for i in range(len(self.steps)):
            if not self.check_step(i):
                return False, i
        return True, 0

    def check_step(self, step_id: int) -> bool:
        step = self.get_step(step_id)
        if step is None:
            return False
        
        # is Assumption
        if isinstance(step.proof_type, Assumption):
            if not (0 <= step.proof_type.index < len(self.context)):
                return False
            return step.formula == self.context[step.proof_type.index]
        
        # is Axiom
        if isinstance(step.proof_type, Axiom):
            return step.proof_type.fit_expr(step.formula)
        
        # is MP
        if isinstance(step.proof_type, MP):
            id1, id2 = step.proof_type.index1, step.proof_type.index2
            step1, step2 = self.get_step(id1), self.get_step(id2)
            if (step1 is None) or (step2 is None):
                return False
            return step1.formula == Impl(step2.formula, step.formula)
        

        return False
    
    def get_step(self, step_id) -> Optional[ProofStep]:
        if (step_id < 0) or (step_id >= len(self.steps)):
            return None
        return self.steps[step_id]
    
    def show_step(self, step_id: int) -> Optional[str]:
        step = self.get_step(step_id)
        if step is None:
            return None
        G = ", ".join([f"{e}" for e in self.context])
        if G != "":
            G += " "
        return f"{G}|- {step.formula} [{step.proof_type}]"

        