from logic import Proof, ProofStep, Axiom, MP
from logic.expr import I, O, V

# |- (A or B) -> (B or A)
def proof_or_swap() -> Proof: 
    proof = Proof(
        [],
        [
            # |- (A -> B or A) -> (B -> B or A) -> (A or B -> B or A)
            ProofStep(
                I(I(V("A"), V("C")), I(I(V("B"), V("C")), I(O(V("A"), V("B")), V("C")))).replace({"C": O(V("B"), V("A"))}), 
                Axiom(7)
            ),
            ProofStep(I(V("A"), O(V("A"), V("B"))).replace({"B": V("A"), "A": V("B")}), Axiom(5)),
            ProofStep(I(V("B"), O(V("A"), V("B"))).replace({"B": V("A"), "A": V("B")}), Axiom(6)),
            ProofStep(
                I(I(V("B"), V("C")), I(O(V("A"), V("B")), V("C"))).replace({"C": O(V("B"), V("A"))}),
                MP(0, 2)
            ),
            ProofStep(
                I(O(V("A"), V("B")), V("C")).replace({"C": O(V("B"), V("A"))}),
                MP(3, 1)
            )
        ]
    )

    assert proof.is_correct()[0]
    return proof
