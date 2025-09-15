from logic.proof import Proof
from logic.context import Context, add_to_context

def advance_context_theorem(p: Proof, context: Context) -> Proof:
    return Proof(
        context=add_to_context(p.context, context),
        steps=p.steps
    )