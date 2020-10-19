import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()

from data import vacancies, companies, specialties
from jumanji.models import Vacancy, Company, Specialty
from datetime import datetime

Vacancy.objects.all().delete()
Company.objects.all().delete()
Specialty.objects.all().delete()


for com in companies:
    company = Company.objects.create(title=com['title'])

for spec in specialties:
    specialty = Specialty.objects.create(
        code = spec['code'],
        title = spec['title'],
        picture = ''
    )

for vac in vacancies:
    date = datetime.strptime(vac['posted'], "%Y-%m-%d")
    vacancy = Vacancy.objects.create(
        title = vac['title'],
        specialty = Specialty.objects.get(code=vac['cat']),
        company = Company.objects.get(title=vac['company']),
        salary_min = vac['salary_from'],
        salary_max = vac['salary_to'],
        published_at = date,
        description = vac['desc']
    )