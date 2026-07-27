from django.shortcuts import render
from .models import Resume
from .utils import extract_pdf_text


def upload_resume(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        resume_file = request.FILES['resume_file']

        extracted_text = extract_pdf_text(resume_file)

        Resume.objects.create(
            name=name,
            email=email,
            resume_file=resume_file,
            extracted_text=extracted_text
        )

    return render(request, "upload.html")