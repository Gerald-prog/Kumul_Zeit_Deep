import json
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    EXE_DIR = Path(sys.executable).parent
else:
    EXE_DIR = Path(__file__).parent

CONFIG_DATEI = EXE_DIR / "config.json"


def lade_config() -> dict:
    if not CONFIG_DATEI.exists():
        return {}
    try:
        return json.loads(CONFIG_DATEI.read_text(encoding="utf-8"))
    except Exception:
        return {}


def speichere_config(config: dict) -> None:
    CONFIG_DATEI.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_DATEI.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
