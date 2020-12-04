from django.contrib.auth import get_user_model
from django.db import models

from conf.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


class Company(models.Model):

    title = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField(max_length=1200)
    employee_count = models.IntegerField()
    owner = models.OneToOneField(get_user_model(), related_name='company', on_delete=models.CASCADE)


class Specialty(models.Model):

    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)


class Vacancy(models.Model):

    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now_add=True)
    skills = models.CharField(max_length=600)
    description = models.CharField(max_length=5000)


class Application(models.Model):

    written_username = models.CharField(max_length=64)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField(max_length=1200)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='applications')


class Resume(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    status = models.CharField(max_length=64)
    salary = models.IntegerField()
    specialty = models.CharField(max_length=64)
    qualification = models.CharField(max_length=64)
    education = models.CharField(max_length=64)
    experience = models.TextField(max_length=5000)
    portfolio = models.CharField(max_length=64)
