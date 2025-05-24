from django.db import models


# Create your models here.
class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    required_skills = models.TextField(default=list)
    posting_date = models.DateField()
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"
