from django.shortcuts import render
from .models import Resume
from .utils import extract_pdf_text, extract_skills, calculate_score


def upload_resume(request):
    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        resume_file = request.FILES["resume_file"]

        # Extract text
        extracted_text = extract_pdf_text(resume_file)

        # Detect skills
        skills = extract_skills(extracted_text)

        # Calculate score
        score = calculate_score(skills)

        # 👇 Add these debug prints here
        print("Extracted Text:")
        print(extracted_text)

        print("Detected Skills:")
        print(skills)

        print("Score:")
        print(score)

        # Save to database
        Resume.objects.create(
            name=name,
            email=email,
            resume_file=resume_file,
            extracted_text=extracted_text,
            skills=", ".join(skills),
            score=score,
        )

    return render(request, "upload.html")