from logic.proof import Proof

def print_proof(proof: Proof, file = None):
    if proof.is_correct()[0]:
        number_of_digits = len(f"{len(proof.steps)}")
        def index_str(i: int) -> str:
            s = f"{i}"
            s += "".join([" " for _ in range(number_of_digits - len(s))])
            return s

        for i in range(len(proof.steps)):
            print(f"{index_str(i)}", proof.show_step(i), file=file)
        print("", file=file)
        
    print(f"CORRECT: {proof.is_correct()}", file=file)
