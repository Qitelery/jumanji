from django.shortcuts import render
from django.views import View
from jumanji.models import Vacancy, Company, Specialty
from django.db.models import Count


class MainView(View):

    def get(self, request):

        specials_on_main = Specialty.objects.annotate(vac_count = Count('vacancies')).all()
        return render(request, 'jumanji/index.html', context = {'specials_on_main': specials_on_main})

class ListVacancies(View):

    def get(self, request):

        return render(request, 'jumanji/vacancies.html')

class SpecVacancies(View):

    def get(self, request):

        return render(request, 'jumanji/vacancies.html')

class CompanyCard(View):

    def get(self, request):

        return render(request, 'jumanji/company.html')

class Vacancy(View):

    def get(self, request):

        return render(request, 'jumanji/vacancy.html')
