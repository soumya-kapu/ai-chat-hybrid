from pathlib import Path


def test_ai_chat_file_exists():
    assert Path("ai_chat.py").exists()
