import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from helpers.constants import EMPLOYMENT_TYPES, THESIS_EMPLOYMENT_TYPE_KEYWORDS
from common.llm_service import get_groq
from helpers.utils import list_to_str
from models.employment_check import EmploymentCheck

from langchain_core.messages import SystemMessage, HumanMessage


def get_classifier_system_prompt() -> str:
    return f"""You classify job ads from the Swedish job board Platsbanken.

The ad's title does not name a thesis, but the description mentions one
({list_to_str(EMPLOYMENT_TYPES)}). Decide from the description whether the ad
actually offers a thesis to a student, or only mentions theses in passing.

has_matched=true: the reader is invited to do their thesis here.
has_matched=false: the ad offers another position (regular job, PhD, postdoc,
lecturer, consultant) and only mentions theses, e.g. supervising thesis students.
Ads may be in Swedish or English.

Examples:

Title: Pallperception med deep learning
Ad: Vi söker en masterstudent som vill göra sitt examensarbete på 30 hp hos oss...
Answer: has_matched=true (the reader is invited to do a thesis)

Title: AI for predictive maintenance at our plant
Ad: We offer a master's student the opportunity to write their thesis on...
Answer: has_matched=true (the reader is invited to do a thesis)

Title: Postdoktor avancerad karakterisering kolmaterial
Ad: ...delta i handledning och undervisning av exjobb och doktorander...
Answer: has_matched=false (a postdoc; it mentions supervising thesis students)

Title: Doktorand inom Tillförlitliga Edge Beräkningar och Nätverk
Ad: Egen forskarutbildning ... beräknas leda fram till en licentiatexamen...
Answer: has_matched=false (a PhD position, not a master's thesis)

Title: Junior Data Engineer
Ad: ...You might have experience with school projects, internships, thesis work...
Answer: has_matched=false (a regular job; theses are mentioned in passing)"""


def get_classifier_human_prompt(title, desc):
    return f"Title: {title}\n\nAd:\n{desc}"


classifier = get_groq(max_tokens=100).with_structured_output(EmploymentCheck)

def classify_thesis(title, desc) -> bool:
    try:
        result = classifier.invoke([
            SystemMessage(content=get_classifier_system_prompt()),
            HumanMessage(content=get_classifier_human_prompt(title, desc)),
        ])
        return bool(result.has_matched)
    except Exception as exc:
        print(f"Classifier failed for '{title[:50]}': {exc}")
        return False


def is_thesis_ad(title: str, desc: str) -> bool:
    title = title.lower()
    desc = desc.lower()

    if any(emp_type in title for emp_type in THESIS_EMPLOYMENT_TYPE_KEYWORDS):
        return True   

    if any(emp_type in desc for emp_type in THESIS_EMPLOYMENT_TYPE_KEYWORDS):
        return classify_thesis(title=title, desc=desc)

    return False