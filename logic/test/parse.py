from logic.expr import parse_expr, I, O, A, V, N, Expr, ParsingError

def run_parsing_test():
    def test_correct_parsing(input: str, expected: Expr) -> bool:
        parse_result = parse_expr(input)

        if isinstance(parse_result, ParsingError):
            print(f"Error: {parse_result.message}")
            return False
        else:
            if parse_result == expected:
                print(f"Test \"{input}\" SUCCESS")
                return True
            print("Error: results are not same")
            print(f"\tExpected: {expected}")
            print(f"\tGot:      {parse_result}")
            return False
            

    assert test_correct_parsing("A", V("A"))
    assert test_correct_parsing("(A)", V("A"))
    assert test_correct_parsing("A -> B", I(V("A"), V("B")))
    assert test_correct_parsing("A -> (B -> C)", I(V("A"), I(V("B"), V("C"))))
    assert test_correct_parsing("(A -> B) -> C", I(I(V("A"), V("B")), V("C")))
    assert test_correct_parsing("A -> B -> C", I(V("A"), I(V("B"), V("C"))))
    assert test_correct_parsing("A & (B & C)", A(V("A"), A(V("B"), V("C"))))
    assert test_correct_parsing("A & B & C", A(A(V("A"), V("B")), V("C")))
    assert test_correct_parsing("A | (B | C)", O(V("A"), O(V("B"), V("C"))))
    assert test_correct_parsing("A | B | C", O(O(V("A"), V("B")), V("C")))
    assert test_correct_parsing("A | (B & C)", O(V("A"), A(V("B"), V("C"))))
    assert test_correct_parsing("A | B & C", O(V("A"), A(V("B"), V("C"))))
    assert test_correct_parsing("A & B | C", O(A(V("A"), V("B")), V("C")))
    assert test_correct_parsing("!A", N(V("A")))
    assert test_correct_parsing("!!A", N(N(V("A"))))
    assert test_correct_parsing("!!(!!A)", N(N(N(N(V("A"))))))
    assert test_correct_parsing("!A -> B", I(N(V("A")), V("B")))
    assert test_correct_parsing("A | B -> C & D", I(O(V("A"), V("B")), A(V("C"), V("D"))))
    assert test_correct_parsing("A -> B | !C & D", I(V("A"), O(V("B"), A(N(V("C")), V("D")))))
    assert test_correct_parsing("A -> (B | !C & D)", I(V("A"), O(V("B"), A(N(V("C")), V("D")))))
    assert test_correct_parsing("A -> B | (!C & D)", I(V("A"), O(V("B"), A(N(V("C")), V("D")))))
    assert test_correct_parsing("(A) -> (B) | (!C & (D))", I(V("A"), O(V("B"), A(N(V("C")), V("D")))))
    
    
    
    
    
    
    
    
    
    