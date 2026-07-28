from django.db import models


class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume_file = models.FileField(upload_to="resumes/")
    extracted_text = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    score = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
