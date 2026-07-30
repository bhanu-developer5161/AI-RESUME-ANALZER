import PyPDF2
from .skills import SKILLS


def extract_pdf_text(file):
    """
    Extract text from uploaded PDF.
    """
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(file)

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print("PDF Extraction Error:", e)

    return text


def extract_skills(text):
    """
    Detect skills from resume text.
    """
    found_skills = []

    if not text:
        return found_skills

    text = text.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_score(text, skills, name, email):
    """
    Calculate ATS Resume Score.
    """

    score = 0

    # Skills Score (Maximum 40)
    score += min(len(skills) * 5, 40)

    # Resume Length (Maximum 20)
    if len(text) >= 500:
        score += 20
    elif len(text) >= 250:
        score += 10

    # Name Present
    if name:
        score += 10

    # Email Present
    if email:
        score += 10

    # Keyword Score (Maximum 20)
    keyword_score = 0

    for skill in SKILLS:
        if skill.lower() in text.lower():
            keyword_score += 2

    score += min(keyword_score, 20)

    return min(score, 100)


def find_missing_skills(found_skills):
    """
    Find missing skills from predefined skill list.
    """

    missing = []

    for skill in SKILLS:
        if skill not in found_skills:
            missing.append(skill)

    return missing