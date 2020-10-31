from django.shortcuts import render
from django.views import View
from jumanji.forms import SendForm
from jumanji.models import Vacancy, Company, Specialty, Application
from django.db.models import Count


class MainView(View):

    def get(self, request):

        specials_on_main = Specialty.objects.annotate(vac_count=Count('vacancies')).all()
        company_on_main = Company.objects.annotate(vac_count=Count('vacancies')).all()
        return render(request, 'jumanji/index.html',
                      context={'specials_on_main': specials_on_main,
                               'company_on_main': company_on_main})


class EntryPoint(View):

    def get(self, request):
        return render(request, 'jumanji/login.html')


class ListVacancies(View):

    def get(self, request):

        lst_vac = Vacancy.objects.all()
        return render(request, 'jumanji/vacancies.html', context={'lst_vac': lst_vac})


class SpecVacancies(View):

    def get(self, request, cat_id):

        speca = Specialty.objects.get(id=cat_id)
        spec_vacan = Vacancy.objects.filter(specialty_id=cat_id)
        return render(request, 'jumanji/spec_vacancies.html',
                      context={'spec_vacan': spec_vacan,
                               'speca': speca})


class CompanyCard(View):

    def get(self, request, com_id):

        compa = Company.objects.get(id=com_id)
        vacan_of_company = Vacancy.objects.filter(company_id=com_id)
        return render(request, 'jumanji/company.html',
                      context={'compa': compa,
                               'vacan_of_company': vacan_of_company})


class OneVacancy(View):

    def get(self, request, vac_id):

        one_vac = Vacancy.objects.get(id=vac_id)
        compa_of_one_vac = Company.objects.get(id=one_vac.company_id)
        return render(request, 'jumanji/vacancy.html',
                      context={'one_vac': one_vac,
                               'compa_of_one_vac': compa_of_one_vac})


class SendApply(View):

    def post(self, request, vac_id):

        vacancy = Vacancy.objects.get(id=vac_id)
        owner = Company.objects.get(id=vacancy.company_id)
        form = SendForm(request.POST)
        if form.is_valid():
            Application.objects.create(written_username=form.username,
                                       written_phone=form.telephone,
                                       written_cover_letter=form.cover_letter,
                                       vacancy=vac_id,
                                       user=owner.owner_id)
            return render(request, 'jumanji/vacancy.html')
        return render(request, 'jumanji/vacancy.html',
                      context={'one_vac': vacancy,
                               'compa_of_one_vac': owner})
