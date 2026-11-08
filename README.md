# CASE NULL: THE FINAL STATE

An automata-driven detective investigation game for Formal Languages and Automata.

## Setup (Windows PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m game.main
```

If PowerShell blocks activation, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe -m game.main` instead.

## Test

```powershell
python -m pytest -q
```

## Architecture

- `game/`: Pygame presentation and interactions
- `engine/`: formal automata execution and game state
- `automata/`: JFLAP source-of-truth models (`.jff`)
- `data/`: case definitions and evidence
- `assets/`: original/licensed visual and audio assets
- `tests/`: regression and model-equivalence tests
- `docs/`: technical design, rubrics and demo evidence

The first executable is a repository smoke test, **not** the finished detective game. Formal models, case logic and visuals will be integrated next. Do not represent it as completed functionality.
