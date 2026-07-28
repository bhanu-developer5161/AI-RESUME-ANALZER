import PyPDF2
from .skills import SKILLS


def extract_pdf_text(file):
    """
    Extract text from a PDF file.
    """
    text = ""

    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_skills(text):
    """
    Detect skills from extracted resume text.
    """
    found_skills = []

    if not text:
        return found_skills

    text = text.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_score(skills):
    """
    Calculate resume score based on detected skills.
    """
    total_skills = len(SKILLS)

    if total_skills == 0:
        return 0

    score = (len(skills) / total_skills) * 100

    return round(score)