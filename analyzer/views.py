from django.shortcuts import render
from .models import Resume
from .utils import extract_pdf_text, extract_skills

def upload_resume(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        resume_file = request.FILES.get('resume_file')

        if resume_file:
            # 1. Extract text
            extracted_text = extract_pdf_text(resume_file)
            
            # Reset file pointer so Django saves the file contents properly
            resume_file.seek(0)

            # 2. Extract skills
            skills = extract_skills(extracted_text) or []

            # Print for debugging in terminal
            print("RESUME TEXT:", extracted_text)
            print("FOUND SKILLS:", skills)

            # 3. Format skills properly (handles lists or single strings)
            if isinstance(skills, list):
                skills_str = ", ".join(skills)
            else:
                skills_str = str(skills)

            # 4. Save to database
            Resume.objects.create(
                name=name,
                email=email,
                resume_file=resume_file,
                extracted_text=extracted_text,
                skills=skills_str
            )

    return render(request, "upload.html")