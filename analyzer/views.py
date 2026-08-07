from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Resume
from .utils import extract_pdf_text
from .utils import (
    extract_skills,
    calculate_score,
    find_missing_skills,
    generate_ai_suggestions,
    calculate_job_match
)



# ----------------------------
# Register
# ----------------------------

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")


        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists"
            )

            return redirect("register")


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()


        messages.success(
            request,
            "Registration successful"
        )

        return redirect("login")


    return render(
        request,
        "register.html"
    )



# ----------------------------
# Login
# ----------------------------

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user:

            login(
                request,
                user
            )


            return redirect(
                "dashboard"
            )


        else:

            messages.error(
                request,
                "Invalid username or password"
            )


    return render(
        request,
        "login.html"
    )



# ----------------------------
# Logout
# ----------------------------

@login_required
def logout_view(request):

    logout(request)

    return redirect(
        "login"
    )



# ----------------------------
# Dashboard
# ----------------------------

@login_required
def dashboard(request):

    resumes = Resume.objects.filter(
        email=request.user.email
    )


    return render(
        request,
        "dashboard.html",
        {
            "resumes": resumes
        }
    )



# ----------------------------
# Upload Resume
# ----------------------------

@login_required
def upload_resume(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        resume_file = request.FILES.get("resume_file")


        if resume_file:


            # Create resume record
            resume = Resume.objects.create(
                name=name,
                email=email,
                resume_file=resume_file
            )


            # 1. Extract PDF text
            extracted_text = extract_pdf_text(
                resume_file
            )


            # 2. Detect skills
            skills = extract_skills(
                extracted_text
            )


            # 3. Calculate ATS score
            score = calculate_score(
                extracted_text,
                skills,
                name,
                email
            )


            # 4. Find missing skills
            missing_skills = find_missing_skills(
                skills
            )

            # 5. Generate AI suggestions
            ai_suggestions = generate_ai_suggestions(
             score,
             missing_skills
           )

            # Save analysis


            resume.extracted_text = extracted_text

            resume.skills = ", ".join(skills)

            resume.score = score

            resume.missing_skills = ", ".join(missing_skills)

            print("Extracted Text:", extracted_text[:200])
            print("Detected Skills:", skills)
            print("ATS Score:", score)
            print("Missing Skills:", missing_skills)
            resume.save()   # <-- THIS SAVES TO DATABASE


            return redirect(
                "dashboard"
            )


    return render(
        request,
        "upload.html"
    )



# ----------------------------
# Resume History
# ----------------------------

@login_required
def resume_history(request):

    resumes = Resume.objects.filter(
        email=request.user.email
    ).order_by(
        "-uploaded_at"
    )


    return render(
        request,
        "resume_history.html",
        {
            "resumes": resumes
        }
    )



# ----------------------------
# Resume Analysis Details
# ----------------------------

@login_required
def resume_analysis(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id
    )


    # Detected skills
    skills = []

    if resume.skills:
        skills = [
            skill.strip()
            for skill in resume.skills.split(",")
        ]


    # Missing skills
    missing_skills = []

    if resume.missing_skills:
        missing_skills = [
            skill.strip()
            for skill in resume.missing_skills.split(",")
        ]


    # AI Suggestions
    suggestions = generate_ai_suggestions(
        resume.score,
        missing_skills
    )


    # Job Matching

    required_skills = [
        "Python",
        "Django",
        "React",
        "SQL",
        "Git",
        "Docker",
        "REST API"
    ]


    matched, job_missing, job_percentage = calculate_job_match(
        skills,
        required_skills
    )


    return render(
        request,
        "resume_analysis.html",
        {
            "resume": resume,

            "skills": skills,

            "missing_skills": missing_skills,

            "suggestions": suggestions,

            "matched": matched,

            "job_missing": job_missing,

            "job_percentage": job_percentage
        }
    )

# ----------------------------
# Delete Resume
# ----------------------------

@login_required
def delete_resume(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id
    )

    # Delete resume
    resume.delete()

    messages.success(
        request,
        "Resume deleted successfully"
    )

    return redirect(
        "dashboard"
    )

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(
        Resume,
        id=resume_id,
        email=request.user.email
    )

    if resume.resume_file:
        resume.resume_file.delete(save=False)

    resume.delete()

    messages.success(request, "Resume deleted successfully.")

    return redirect("resume_history")