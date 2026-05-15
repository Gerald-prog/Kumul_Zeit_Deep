import json
from pathlib import Path

CONFIG_DATEI = Path(__file__).parent / "config.json"


def lade_config() -> dict:
    if not CONFIG_DATEI.exists():
        return {}
    try:
        return json.loads(CONFIG_DATEI.read_text(encoding="utf-8"))
    except Exception:
        return {}


def speichere_config(config: dict) -> None:
    CONFIG_DATEI.write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
