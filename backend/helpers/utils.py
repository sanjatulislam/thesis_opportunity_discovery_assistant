from datetime import datetime
from zoneinfo import ZoneInfo
import re

def parse_datetime_isoformat(date_str):
    return datetime.fromisoformat(date_str)

def get_datetime_local():
    return datetime.now(ZoneInfo("Europe/Stockholm")).replace(tzinfo=None)

def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\ufeff", "").replace("\u200b", "")
    text = re.sub(r"[ \t]+", " ", text) 
    text = re.sub(r"\n\s*\n+", "\n\n", text) 
    return text.strip()

def list_to_str(data_list: list[str], delimiter: str = ", "):
    return delimiter.join(data_list)