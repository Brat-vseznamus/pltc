from typing import Optional

from logic.expr import I, Expr
from logic.context import remove_from_context

import logic.proof as proof

def deduction_theorem(p: proof.Proof, assumption: Expr) -> Optional[proof.Proof]:
    if assumption not in p.context:
        return None

    # p.context = G & {a}
    a = assumption
    new_p = proof.Proof(list(), list())

    # new_p.context = G
    new_p.context = remove_from_context(p.context, a)
    
    old_id_to_new_id = dict()
    for id, step in enumerate(p.steps):
        current_id = len(new_p.steps)
        f = step.formula
        if isinstance(step.proof_type, proof.Axiom):
            new_p.steps.extend([
                proof.ProofStep(f, step.proof_type),
                proof.ProofStep(I(f, I(a, f)), proof.Axiom(0)),
                proof.ProofStep(I(a, f), proof.MP(current_id + 1, current_id))
            ])
        if isinstance(step.proof_type, proof.Assumption):
            if step.formula == a:
                # a -> a
                new_p.steps.extend([
                    proof.ProofStep(I(f, I(f, f)), proof.Axiom(0)),
                    proof.ProofStep(I(I(f, I(f, f)), I(I(f, I(I(f, f), f)), I(f, f))), proof.Axiom(1)),
                    proof.ProofStep(I(I(f, I(I(f, f), f)), I(f, f)), proof.MP(current_id + 1, current_id)),
                    proof.ProofStep(I(f, I(I(f, f), f)), proof.Axiom(0)),
                    proof.ProofStep(I(f, f), proof.MP(current_id + 2, current_id + 3))
                ])
            else:
                new_p.steps.extend([
                    proof.ProofStep(f, proof.Assumption()),
                    proof.ProofStep(I(f, I(a, f)), proof.Axiom(0)),
                    proof.ProofStep(I(a, f), proof.MP(current_id + 1, current_id))
                ])
        if isinstance(step.proof_type, proof.MP):
            id1 = step.proof_type.index1
            id2 = step.proof_type.index2
            
            new_id1 = old_id_to_new_id[id1]
            new_id2 = old_id_to_new_id[id2]
            
            f2 = p.steps[id2].formula

            new_p.steps.extend([
                proof.ProofStep(I(I(a, f2), I(I(a, I(f2, f)), I(a, f))), proof.Axiom(1)),
                proof.ProofStep(I(I(a, I(f2, f)), I(a, f)), proof.MP(current_id, new_id2)),
                proof.ProofStep(I(a, f), proof.MP(current_id + 1, new_id1)),
            ])
        
        old_id_to_new_id[id] = len(new_p.steps) - 1
    
    return new_p
