from .formal_models import DFA,NFA,PDA,TuringMachine,regex_accepts,bounded_lba_check

EVIDENCE_DFA=DFA(
 {"q0","q1","q2","q3","q4","q5"},
 {"SCENE","LAB","WITNESS","TIMELINE","MOTIVE"},
 {("q0","SCENE"):"q1",("q1","LAB"):"q2",("q2","WITNESS"):"q3",
  ("q3","TIMELINE"):"q4",("q4","MOTIVE"):"q5"},
 "q0",{"q5"})

SUSPECT_NFA=NFA(
 {"start","forensic","witness","digital","corroborated","closed"},
 {"F","W","D","C"},
 {("start","F"):{"forensic"},("start","W"):{"witness"},("start","D"):{"digital"},
  ("forensic","C"):{"corroborated"},("witness","C"):{"corroborated"},
  ("digital","C"):{"corroborated"},("corroborated","C"):{"closed"}},
 "start",{"closed"})

# Balanced parentheses PDA; stack top is the rightmost character.
BALANCED_PDA=PDA({
 ("q","(","$"):{("q","$(")},("q","(","("):{("q","((")},
 ("q",")","("):{("q","")},("q","","$"):{("f","$")}
},"q","$",{"f"})

# Deterministic single-tape TM recognizing 1^n0^n.
BALANCED_TM=TuringMachine({
 ("q0","X"):("q0","X","R"),("q0","1"):("q1","X","R"),
 ("q0","Y"):("q3","Y","R"),("q0","0"):("rej","0","S"),("q0","_"):("acc","_","S"),
 ("q1","1"):("q1","1","R"),("q1","Y"):("q1","Y","R"),
 ("q1","0"):("q2","Y","L"),("q1","_"):("rej","_","S"),
 ("q2","1"):("q2","1","L"),("q2","0"):("q2","0","L"),
 ("q2","Y"):("q2","Y","L"),("q2","X"):("q2","X","L"),
 ("q2","_"):("q0","_","R"),("q3","Y"):("q3","Y","R"),
 ("q3","_"):("acc","_","S"),("q3","0"):("rej","0","S"),("q3","1"):("rej","1","S")
},"q0","acc","rej")

GRAMMAR={"CASE":[["MOTIVE","METHOD","EVIDENCE"]],
 "MOTIVE":[["GREED"],["REVENGE"],["SILENCE"]],
 "METHOD":[["ACCESS"],["POISON"],["SABOTAGE"]],
 "EVIDENCE":[["TRACE"],["WITNESS"],["RECORD"]]}

def validate_deduction(tokens):
    return (len(tokens)==3 and tokens[0] in {"GREED","REVENGE","SILENCE"}
            and tokens[1] in {"ACCESS","POISON","SABOTAGE"}
            and tokens[2] in {"TRACE","WITNESS","RECORD"})

def derive_deduction(tokens):
    if not validate_deduction(tokens): return []
    motive, method, evidence = tokens
    return ["CASE", "MOTIVE METHOD EVIDENCE",
            f"{motive} METHOD EVIDENCE",
            f"{motive} {method} EVIDENCE",
            f"{motive} {method} {evidence}"]

def validate_case_id(value):
    return regex_accepts(r"CASE-[0-9]{3}:[A-Z]{2,5}",value)
