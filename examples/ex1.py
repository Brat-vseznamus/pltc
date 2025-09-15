

from logic import Proof, ProofStep, Assumption, MP
from logic.expr import I, V

from logic.theorems import deduction_theorem

from logic.utils import print_proof

# A->B->C, A, B |- C
def proof_swap_lemma() -> Proof:
    proof = Proof(
        [V("A"), V("B"), I(V("A"), I(V("B"), V("C")))],
        [
            ProofStep(V("A"), Assumption()),
            ProofStep(V("B"), Assumption()),
            ProofStep(I(V("A"), I(V("B"), V("C"))), Assumption()),
            ProofStep(I(V("B"), V("C")), MP(2, 0)),
            ProofStep(V("C"), MP(3, 1)),
        ]
    )

    assert proof.is_correct()[0]
    return proof

# |- (A->B->C)->(B->A->C)
def proof_swap() -> Proof:
    proof = deduction_theorem(
        deduction_theorem(
            deduction_theorem(
                proof_swap_lemma, 
                V("A")
            ), 
            V("B")
        ), 
        I(V("A"), I(V("B"), V("C")))
    )

    assert proof.is_correct()[0]
    return proof
