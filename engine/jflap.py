import xml.etree.ElementTree as ET
from .formal_models import DFA,NFA

def load_fa(path):
    root=ET.parse(path).getroot(); states=set(); finals=set(); start=None; edges={}
    for s in root.findall(".//state"):
        sid=s.attrib["id"]; states.add(sid)
        if s.find("initial") is not None: start=sid
        if s.find("final") is not None: finals.add(sid)
    alpha=set()
    for t in root.findall(".//transition"):
        src=t.findtext("from"); dst=t.findtext("to"); symbol=t.findtext("read") or ""
        if symbol=="": raise ValueError("Epsilon transitions are not supported by this FA loader.")
        alpha.add(symbol); edges.setdefault((src,symbol),set()).add(dst)
    if start is None: raise ValueError("Missing JFLAP initial state")
    if all(len(v)==1 for v in edges.values()):
        return DFA(states,alpha,{k:next(iter(v)) for k,v in edges.items()},start,finals)
    return NFA(states,alpha,edges,start,finals)
