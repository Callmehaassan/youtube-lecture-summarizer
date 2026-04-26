import os
import json
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history.json")


def load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_history(history: list):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def log_video(video_id: str, title: str, url: str, filepath: str):
    history = load_history()
    entry = {
        "video_id": video_id,
        "title": title,
        "url": url,
        "filepath": filepath,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    # Remove duplicate if exists
    history = [h for h in history if h.get("video_id") != video_id]
    history.insert(0, entry)
    save_history(history)


def get_history() -> list:
    return load_history()


def find_by_video_id(video_id: str) -> dict | None:
    history = load_history()
    for entry in history:
        if entry.get("video_id") == video_id:
            return entry
    return None


def format_history_list() -> str:
    history = load_history()
    if not history:
        return "No lectures summarized yet."
    lines = ["Here are all your summarized lectures:\n"]
    for i, entry in enumerate(history, 1):
        lines.append(f"{i}. {entry['title']}")
        lines.append(f"   Date: {entry['date']}")
        lines.append(f"   File: {entry['filepath']}")
        lines.append(f"   URL: {entry['url']}")
        lines.append("")
    return "\n".join(lines)