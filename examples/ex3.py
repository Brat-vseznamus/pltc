from logic import Proof, ProofStep, Axiom, Assumption, MP, proof_with_lemmas
from logic.expr import I, O, V

from logic.theorems import deduction_theorem

# | A or (B or C) -> (A or B) or C
def proof_distribution() -> Proof:
    # |- A -> (A or B) or C
    proof_left_part = deduction_theorem(
        Proof(
            [V("A")],
            [
                ProofStep(V("A"), Assumption()),
                ProofStep(I(V("A"), O(V("A"), V("B"))), Axiom(5)),
                ProofStep(O(V("A"), V("B")), MP(1, 0)),
                ProofStep(I(O(V("A"), V("B")), O(O(V("A"), V("B")), V("C"))), Axiom(5)),
                ProofStep(O(O(V("A"), V("B")), V("C")), MP(3, 2)),
            ]
        ),
        V("A")
    )

    # |- B -> (A or B) or C
    proof_inner_part = deduction_theorem(
        Proof(
            [V("B")],
            [
                ProofStep(V("B"), Assumption()),
                ProofStep(I(V("B"), O(V("A"), V("B"))), Axiom(6)),
                ProofStep(O(V("A"), V("B")), MP(1, 0)),
                ProofStep(I(O(V("A"), V("B")), O(O(V("A"), V("B")), V("C"))), Axiom(5)),
                ProofStep(O(O(V("A"), V("B")), V("C")), MP(3, 2)),
            ]
        ),
        V("B")
    )

    # |- C -> (A or B) or C
    proof_right_part = deduction_theorem(
        Proof(
            [V("C")],
            [
                ProofStep(V("C"), Assumption()),
                ProofStep(I(V("C"), O(O(V("A"), V("B")), V("C"))), Axiom(6)),
                ProofStep(O(O(V("A"), V("B")), V("C")), MP(1, 0)),
            ]
        ),
        V("C")
    )

    assert proof_left_part.is_correct()[0]
    assert proof_inner_part.is_correct()[0]
    assert proof_right_part.is_correct()[0]

    # | A or (B or C) -> (A or B) or C
    proof = proof_with_lemmas(
        [],
        [
            # |- A -> (A or B) or C
            proof_left_part,
            # |- B -> (A or B) or C
            proof_inner_part,
            # |- C -> (A or B) or C
            proof_right_part,
            # |- (B -> (A or B) or C) -> (C -> (A or B) or C) -> ((B or C) -> (A or B) or C)
            ProofStep(
                Axiom.Axioms[7].replace({
                    "A": V("B"), 
                    "B": V("C"), 
                    "C": O(O(V("A"), V("B")), V("C"))
                }), 
                Axiom(7)
            ),
            # |- (C -> (A or B) or C) -> ((B or C) -> (A or B) or C)
            ProofStep(I(I(V("C"), O(O(V("A"), V("B")), V("C"))), I(O(V("B"), V("C")), O(O(V("A"), V("B")), V("C")))), MP(3, 1)),
            # |- ((B or C) -> (A or B) or C)
            ProofStep(I(O(V("B"), V("C")), O(O(V("A"), V("B")), V("C"))), MP(4, 2)),
            # |- (A -> (A or B) or C) -> ((B or C) -> (A or B) or C) -> (A or (B or C) -> (A or B) or C)
            ProofStep(
                Axiom.Axioms[7].replace({
                    "A": V("A"), 
                    "B": O(V("B"), V("C")), 
                    "C": O(O(V("A"), V("B")), V("C"))
                }), 
                Axiom(7)
            ),
            # |- ((B or C) -> (A or B) or C) -> (A or (B or C) -> (A or B) or C)
            ProofStep(
                I(I(O(V("B"), V("C")), O(O(V("A"), V("B")), V("C"))), I(O(V("A"), O(V("B"), V("C"))), O(O(V("A"), V("B")), V("C")))), 
                MP(6, 0)
            ),
            # |- A or (B or C) -> (A or B) or C
            ProofStep(I(O(V("A"), O(V("B"), V("C"))), O(O(V("A"), V("B")), V("C"))), MP(7, 5)),
        ]
    )

    assert proof.is_correct()
    return proof

