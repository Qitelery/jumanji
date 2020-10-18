from django.shortcuts import render
from django.views import View

class MainView(View):

    def get(self, request):

        return render(request, 'jumanji/index.html')

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
