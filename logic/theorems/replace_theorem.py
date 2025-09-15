from typing import Dict, Optional

from logic.proof import Proof, ProofStep
from logic.expr import Expr

def replace_theorem(proof: Proof, mapping: Dict[str, Expr]) -> Proof:
    return Proof(
        context=[assum.replace(mapping) for assum in proof.context], \
        steps=[ProofStep(step.formula.replace(mapping), step.proof_type) for step in proof.steps]
    )