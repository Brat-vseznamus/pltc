# Python logic theorems checker (PLTC)

## 1. Overview

Library for creating and verifing logic proofs in simple and declarative style.

You can see examples in [examples](examples/):

* [$\vdash A\vee B\to B \vee A$](examples/ex2.py)
* [$\vdash A\vee (B\vee C)\to(A\vee B) \vee C$](examples/ex3.py)
* [$\vdash (A\to B\to C)\to(B\to A \to C)$](examples/ex1.py)

### Basics

[`Expr`](logic/expr.py) - type for expressions (wow) in language, current list of them:

* **Variable(str)** (alias **V**) for variable $A, B, C \dots$
* **Not(Expr)** (alias **N**) for negation $\neg A$
* **Impl(Expr, Expr)** (alias **I**) for implication $A \to B$
* **Or(Expr, Expr)** (alias **O**) for logical disjunction $A \vee B$
* **And(Expr, Expr)** (alias **A**) for logical conjunction $A \wedge B$

Example of usage for expression:
$$ (A \vee \neg B) \to (B \wedge C)$$

Same in python:
```python
Impl(
    Or(
        Variable("A"), 
        Not(Variable("B"))
    ), 
    And(
        Variable("B"), 
        Variable("C")
    )
)
```

[`ProofType`](logic/proof.py) - type for kinds of proof, list of them:

* **Assumption()** for assumptions from context
* [**Axiom(int)**](logic/axioms.py) for axioms (all listed in class)
* **MP(int, int)** for modus ponens where first index stands for step with proof of expression $\alpha \to \beta$ and second for $\alpha$

This type used in ProofStep

[`ProofStep`](logic/proof.py) - type one step in proof which contains `formula` - expression proved on this step and `proof_type` - way of proof this step is corrent

[`Proof`](logic/proof.py) - type which contains `context` - set/list with expression which are assumptions and `steps` - list of proof steps

This type has function `is_corrent` which verifies that each step of proof is correct and return then `(True, 0)` or less `(False, i)` otherwise, where `i` - index with first incorrect step.

Example with proof of
$$\vdash A\vee B\to B \vee A$$

Code:

```python
Proof(
    [],
    [
        # |- (A -> B or A) -> (B -> B or A) -> (A or B -> B or A) Ax. 7
        ProofStep(
            I(I(V("A"), V("C")), I(I(V("B"), V("C")), I(O(V("A"), V("B")), V("C")))).replace({"C": O(V("B"), V("A"))}), 
            Axiom(7)
        ),
        # |- (B -> B or A) Ax. 5
        ProofStep(I(V("A"), O(V("A"), V("B"))).replace({"B": V("A"), "A": V("B")}), Axiom(5)),
        # |- (A -> B or A) Ax. 6
        ProofStep(I(V("B"), O(V("A"), V("B"))).replace({"B": V("A"), "A": V("B")}), Axiom(6)),
        # |- (B -> B or A) -> (A or B -> B or A) MP 0, 2
        ProofStep(
            I(I(V("B"), V("C")), I(O(V("A"), V("B")), V("C"))).replace({"C": O(V("B"), V("A"))}),
            MP(0, 2)
        ),
        # |- A or B -> B or A MP 3, 1
        ProofStep(
            I(O(V("A"), V("B")), V("C")).replace({"C": O(V("B"), V("A"))}),
            MP(3, 1)
        )
    ]
)
```

## 2. Examples

### View results

Lets view how to see proof for example 
$$\vdash A\vee B\to B \vee A$$

Import function [`print_proof`](logic/utils/utils.py) from module `logic.utils`

```python
from examples.ex2 import proof_or_swap
from logic.utils import print_proof

p = proof_or_swap()

print_proof(p)
```

Result of program:

```
0 |- ((A->(B|A))->((B->(B|A))->((A|B)->(B|A)))) [Ax.7]
1 |- (B->(B|A)) [Ax.5]
2 |- (A->(B|A)) [Ax.6]
3 |- ((B->(B|A))->((A|B)->(B|A))) [MP 0, 2]
4 |- ((A|B)->(B|A)) [MP 3, 1]

CORRECT: (True, 0)
```

## 3. Future developing
Some plans here