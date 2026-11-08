from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_directories_exist():
    for directory in ("automata", "engine", "game", "data", "assets", "docs"):
        assert (ROOT / directory).is_dir()


def test_dependencies_declared():
    deps = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert "pygame" in deps and "pytest" in deps
