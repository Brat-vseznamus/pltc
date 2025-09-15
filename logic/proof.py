from typing import List, Union, Tuple, Optional

from logic.expr import Expr, Impl
from logic.axioms import Axiom
from logic.context import Context, context_contains_expr, context_nested
from logic.proof_type import ProofTypeBase

class Assumption(ProofTypeBase):
    def __init__(self):
        pass
        
    def __str__(self):
        return f"Assum."

class MP(ProofTypeBase):
    def __init__(self, index1: int, index2: int):
        self.index1 = index1
        self.index2 = index2
    
    def __str__(self):
        return f"MP {self.index1}, {self.index2}"
    
    def move_by_index(self, shift) -> ProofTypeBase:
        return MP(self.index1 + shift, self.index2 + shift)

ProofType = Union[Axiom, Assumption, MP]

class ProofStep:
    def __init__(self, formula: Expr, proof_type: ProofType):
        self.formula = formula
        self.proof_type = proof_type

class Proof:
    def proof_with_lemmas(context: Context, steps: List[Union[ProofStep, "Proof"]]) -> Optional["Proof"]:
        proof = Proof(context, list())

        old_step_to_new = [0 for _ in range(len(steps))]
        for id, step in enumerate(steps):
            if isinstance(step, ProofStep):
                if isinstance(step.proof_type, MP):
                    if not (0 <= step.proof_type.index1 < id):
                        return None
                    if not (0 <= step.proof_type.index2 < id):
                        return None
                    
                    proof.steps.append(
                        ProofStep(
                            step.formula, 
                            MP(
                                old_step_to_new[step.proof_type.index1],
                                old_step_to_new[step.proof_type.index2]
                            )
                        )
                    )
                else:
                    proof.steps.append(step)
            elif isinstance(step, Proof):
                if not context_nested(step.context, context):
                    return None
                if len(step.steps) == 0:
                    return None

                current_id = len(proof.steps)
                for lemma_step in step.steps:
                    proof.steps.append(
                        ProofStep(
                            lemma_step.formula, 
                            lemma_step.proof_type.move_by_index(current_id)
                        )
                    )
            else:
                return None
            
            old_step_to_new[id] = len(proof.steps) - 1

        return proof

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
            return context_contains_expr(self.context, step.formula)
        
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

        