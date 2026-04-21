import json
import os

PRESET_FILE = "presets.json"
PRESET_VERSION = 1


def load_presets():
    if not os.path.exists(PRESET_FILE):
        return {}

    try:
        with open(PRESET_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_presets(presets):
    with open(PRESET_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)


def upsert_preset(name, mode, data, note=""):
    presets = load_presets()
    presets[name] = {
        "mode": mode,
        "version": PRESET_VERSION,
        "note": note,
        "data": data
    }
    save_presets(presets)


def get_preset(name):
    presets = load_presets()
    return presets.get(name)


def list_presets(mode=None):
    presets = load_presets()
    if mode is None:
        return presets
    return {k: v for k, v in presets.items() if v.get("mode") == mode}


def delete_preset(name):
    presets = load_presets()
    if name in presets:
        del presets[name]
        save_presets(presets)