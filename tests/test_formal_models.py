from engine.case_engine import *
from engine.formal_models import minimize_dfa,bounded_lba_check

def test_dfa_protocol():
    assert EVIDENCE_DFA.accepts(["SCENE","LAB","WITNESS","TIMELINE","MOTIVE"])
    assert not EVIDENCE_DFA.accepts(["LAB","SCENE"])

def test_nfa_subset_construction():
    d=SUSPECT_NFA.to_dfa()
    for w in (["F","C","C"],["W","C","C"],["D","C","C"],["F"],["X"]):
        assert SUSPECT_NFA.accepts(w)==d.accepts(w)

def test_minimization_language_preserved():
    d=SUSPECT_NFA.to_dfa(); m=minimize_dfa(d)
    for w in ([],["F"],["F","C"],["F","C","C"],["W","C","C"],["D","C","C"]):
        assert d.accepts(w)==m.accepts(w)

def test_pda_balanced_parentheses():
    assert BALANCED_PDA.accepts("()")
    assert BALANCED_PDA.accepts("(())")
    assert not BALANCED_PDA.accepts("(()")

def test_tm_equal_unary_counts():
    assert BALANCED_TM.run("1100")["accepted"]
    assert not BALANCED_TM.run("110")["accepted"]

def test_lba_bounded_language():
    assert bounded_lba_check("XXYY")
    assert not bounded_lba_check("XYXY")
    assert not bounded_lba_check("XXY")

def test_regex_case_id():
    assert validate_case_id("CASE-417:AX")
    assert not validate_case_id("CASE-41:AX")

def test_cfg_deduction():
    assert validate_deduction(["GREED","POISON","TRACE"])
    assert not validate_deduction(["GREED","UNKNOWN","TRACE"])
