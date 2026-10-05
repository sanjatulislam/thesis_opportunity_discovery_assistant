from datetime import datetime
from zoneinfo import ZoneInfo
import re

def parse_datetime_isoformat(date_str):
    return datetime.fromisoformat(date_str)

def get_datetime_local():
    return datetime.now(ZoneInfo("Europe/Stockholm")).replace(tzinfo=None)

def clean_text(text: str) -> str:
    for ch in ("\xa0", "\u202f"):                
        text = text.replace(ch, " ")
    for ch in ("\ufeff", "\u200b", "\xad"):       
        text = text.replace(ch, "")
    text = re.sub(r"[ \t]+", " ", text)           
    text = re.sub(r" *\n *", "\n", text)       
    text = re.sub(r"\n{3,}", "\n\n", text)      
    return text.strip()

def list_to_str(data_list: list[str], delimiter: str = ", "):
    return delimiter.join(data_list)