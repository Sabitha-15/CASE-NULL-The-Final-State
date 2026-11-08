# CASE NULL — Build 01: Formal Engine

This build adds executable DFA, NFA, subset construction, DFA minimization,
regular-expression validation, PDA, bounded LBA-style recognition, and a
single-tape deterministic Turing Machine. It also adds a starter CFG for
structured final deductions and a JFLAP `.jff` finite-automaton loader.

## Install / test
```powershell
python -m pip install pytest
python -m pytest -q
```

The existing Pygame UI is not replaced in this build. This is the computation
layer that the next integration step will connect to the investigation screens.

Important: the LBA component is a bounded recognizer for a specified language,
not a universal LBA simulator. The PDA and TM are executable simulators.
