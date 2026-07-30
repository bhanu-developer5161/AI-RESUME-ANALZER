from django.shortcuts import render
from .models import Resume
from .utils import (
    extract_pdf_text,
    extract_skills,
    calculate_score,
    find_missing_skills,
)


def upload_resume(request):
    if request.method == "POST":

        # Get form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        resume_file = request.FILES.get("resume_file")

        # Extract text from PDF
        extracted_text = extract_pdf_text(resume_file)

        # Detect skills
        skills = extract_skills(extracted_text)

        # Find missing skills
        missing_skills = find_missing_skills(skills)

        # Calculate ATS Score
        score = calculate_score(
            extracted_text,
            skills,
            name,
            email
        )

        # Save resume details
        Resume.objects.create(
            name=name,
            email=email,
            resume_file=resume_file,
            extracted_text=extracted_text,
            skills=", ".join(skills),
            missing_skills=", ".join(missing_skills),
            score=score,
        )

        # Send data to template
        context = {
            "success": True,
            "name": name,
            "email": email,
            "skills": skills,
            "missing_skills": missing_skills,
            "score": score,
        }

        return render(request, "upload.html", context)

    return render(request, "upload.html")