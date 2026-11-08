from collections import defaultdict, deque
from dataclasses import dataclass
import re

@dataclass
class DFA:
    states:set; alphabet:set; transitions:dict; start:str; finals:set
    def accepts(self, word):
        q=self.start
        for a in word:
            q=self.transitions.get((q,a))
            if q is None: return False
        return q in self.finals
    def trace(self, word):
        q=self.start; out=[q]
        for a in word:
            q=self.transitions.get((q,a))
            if q is None: return out+["REJECT"]
            out.append(q)
        return out+["ACCEPT" if q in self.finals else "REJECT"]

@dataclass
class NFA:
    states:set; alphabet:set; transitions:dict; start:str; finals:set
    def accepts(self, word):
        current={self.start}
        for a in word:
            current={d for q in current for d in self.transitions.get((q,a),set())}
        return bool(current & self.finals)
    def to_dfa(self):
        start=frozenset([self.start]); queue=deque([start]); seen={start}
        name={start:"{" + ",".join(sorted(start)) + "}"}; trans={}; finals=set()
        while queue:
            subset=queue.popleft(); src=name[subset]
            if subset & self.finals: finals.add(src)
            for a in self.alphabet:
                target=frozenset(d for q in subset for d in self.transitions.get((q,a),set()))
                if target not in seen:
                    seen.add(target); queue.append(target)
                    name[target]="{" + ",".join(sorted(target)) + "}"
                trans[(src,a)]=name[target]
        return DFA(set(name.values()),set(self.alphabet),trans,name[start],finals)

def minimize_dfa(dfa):
    states=set(dfa.states)|{"__DEAD__"}; alpha=sorted(dfa.alphabet)
    trans={(q,a):dfa.transitions.get((q,a),"__DEAD__") for q in states for a in alpha}
    parts=[p for p in (set(dfa.finals),states-set(dfa.finals)) if p]
    changed=True
    while changed:
        changed=False; refined=[]
        for part in parts:
            buckets=defaultdict(set)
            for q in part:
                sig=tuple(next(i for i,p in enumerate(parts) if trans[(q,a)] in p) for a in alpha)
                buckets[sig].add(q)
            refined.extend(buckets.values()); changed |= len(buckets)>1
        parts=refined
    idx={q:i for i,p in enumerate(parts) for q in p}; names={i:f"M{i}" for i in range(len(parts))}
    out={(names[i],a):names[idx[trans[(next(iter(p)),a)]]] for i,p in enumerate(parts) for a in alpha}
    return DFA(set(names.values()),set(dfa.alphabet),out,names[idx[dfa.start]],{names[idx[q]] for q in dfa.finals})

def regex_accepts(pattern, text):
    return re.fullmatch(pattern,text) is not None

@dataclass
class PDA:
    # transitions[(state, input-or-epsilon, stack-top)] = {(next-state, replacement)}
    transitions:dict; start:str; initial_stack:str; finals:set
    def accepts(self, word, max_steps=10000):
        todo=deque([(self.start,0,self.initial_stack,0)]); seen=set()
        while todo:
            q,pos,stack,steps=todo.popleft()
            if steps>max_steps: continue
            conf=(q,pos,stack)
            if conf in seen: continue
            seen.add(conf)
            if pos==len(word) and q in self.finals: return True
            if not stack: continue
            for a in ("", word[pos] if pos<len(word) else None):
                if a is None: continue
                for nq,repl in self.transitions.get((q,a,stack[-1]),set()):
                    todo.append((nq,pos+(a!=""),stack[:-1]+repl,steps+1))
        return False

@dataclass
class TuringMachine:
    transitions:dict; start:str; accept:str; reject:str; blank:str="_"
    def run(self, word, max_steps=5000):
        tape=list(word) or [self.blank]; head=0; q=self.start; steps=0; history=[]
        while q not in (self.accept,self.reject) and steps<max_steps:
            if head<0: tape.insert(0,self.blank); head=0
            if head>=len(tape): tape.append(self.blank)
            history.append((q,"".join(tape),head))
            rule=self.transitions.get((q,tape[head]))
            if rule is None: q=self.reject; break
            nq,write,move=rule; tape[head]=write; q=nq
            head += {"L":-1,"R":1,"S":0}[move]; steps+=1
        return {"accepted":q==self.accept,"state":q,"tape":"".join(tape),
                "head":head,"steps":steps,"history":history,"timed_out":steps>=max_steps}

def bounded_lba_check(word, bound=64):
    # Bounded recognizer for X^nY^n, with input confined to its original cells.
    if len(word)>bound or any(c not in "XY" for c in word): return False
    seen_y=False; x=y=0
    for c in word:
        if c=="Y": seen_y=True; y+=1
        elif seen_y: return False
        else: x+=1
    return x==y
