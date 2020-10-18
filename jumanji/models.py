from django.db import models
from django.db.models import CharField, ForeignKey, IntegerField


class Company(models.Model):

    title = models.CharField(max_length=64)


class Specialty(models.Model):

    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.CharField(max_length=64)


class Vacancy(models.Model):

    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
    description = models.CharField(max_length=64)