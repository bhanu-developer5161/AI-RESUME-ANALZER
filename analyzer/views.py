from django.shortcuts import render, redirect, get_object_or_404

from .models import Resume

from .utils import (
    extract_pdf_text,
    extract_skills,
    calculate_score,
    find_missing_skills,
    generate_ai_suggestions,
    JOB_SKILLS,
    calculate_job_match,
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
            email,
        )

        # Generate AI Suggestions
        ai_suggestions = generate_ai_suggestions(
            score,
            missing_skills,
        )

        # Save Resume
        resume = Resume.objects.create(
            name=name,
            email=email,
            resume_file=resume_file,
            extracted_text=extracted_text,
            skills=", ".join(skills),
            missing_skills=", ".join(missing_skills),
            score=score,
        )

        # Redirect to Dashboard
        return redirect("dashboard", resume.id)

    return render(request, "upload.html")


def dashboard(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id
    )

    ai_suggestions = generate_ai_suggestions(
        resume.score,
        resume.missing_skills.split(", ")
        if resume.missing_skills else []
    )

    matched, job_missing, job_percentage = calculate_job_match(
        resume.skills.split(", "),
        JOB_SKILLS,
    )

    context = {
        "resume": resume,
        "ai_suggestions": ai_suggestions,
        "matched": matched,
        "job_missing": job_missing,
        "job_percentage": job_percentage,
    }

    return render(request, "dashboard.html", context)

def resume_history(request):

    resumes = Resume.objects.all().order_by("-id")

    context = {
        "resumes": resumes
    }

    return render(
        request,
        "history.html",
        context
    )