from django.shortcuts import render
from .models import Resume


def upload_resume(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        resume_file = request.FILES['resume_file']

        Resume.objects.create(
            name=name,
            email=email,
            resume_file=resume_file
        )

    return render(request, "upload.html")