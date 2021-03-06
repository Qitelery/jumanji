from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from jumanji.forms import SendForm, Registration, LogInForm, SearchForm, EditOwnCompany, ResumeForm, VacancyForm
from jumanji.models import Vacancy, Company, Specialty, Application, Resume
from django.db.models import Count, Q


class MainView(View):

    def get(self, request):

        specials_on_main = Specialty.objects.annotate(vac_count=Count('vacancies')).all()
        company_on_main = Company.objects.annotate(vac_count=Count('vacancies')).all()
        return render(request, 'jumanji/index.html',
                      context={'specials_on_main': specials_on_main,
                               'company_on_main': company_on_main})


class RegistrationPost(View):

    def get(self, request):

        return render(request, 'jumanji/register.html')

    def post(self, request):

       if request.method == 'POST':
           register_form = Registration(request.POST)
           if register_form.is_valid():
               data = register_form.cleaned_data
               get_user_model().objects.create_user(username=data['login'],
                                                    first_name=data['name'],
                                                    last_name=data['surname'],
                                                    password=data['password'])
               return redirect(reverse('login'))


class LogIn(View):

    def get(self, request):

        return render(request, 'jumanji/login.html')

    def post(self, request):

        if request.method == 'POST':
            login_form = LogInForm(request.POST)
            if login_form.is_valid():
                data = login_form.cleaned_data
                user = authenticate(request, username=data['login'], password=data['password'])
                if user is not None:
                    owner = get_user_model().objects.get(username=data['login'])
                    company = Company.objects.filter(owner=owner.id).first()
                    if company is None:
                        login(request, user)
                        return render(request, 'jumanji/company-create.html')
                    else:
                        login(request, user)
                        return redirect('/')


class LogOut(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class ListVacancies(View):

    def get(self, request):

        lst_vac = Vacancy.objects.all()
        lst_companies = Company.objects.all()
        vacancies_amount = len(lst_vac)
        return render(request, 'jumanji/vacancies.html', context={'lst_vac': lst_vac,
                                                                  'lst_companies': lst_companies,
                                                                  'vacancies_amount': vacancies_amount})


class Search(View):

    def post(self, request):

        if request.method == 'POST':
            search_form = SearchForm(request.POST)
            if search_form.is_valid() and search_form is not None:
                search_data = search_form.cleaned_data
                searched_vacancies = Vacancy.objects.filter(Q(title__icontains=search_data['search_string']) |
                                                            Q(description__icontains=search_data['search_string']) |
                                                            Q(skills__icontains=search_data['search_string']))
                vacancies_count = len(searched_vacancies)
                companies = Company.objects.all()
                return render(request, 'jumanji/search.html', context={'searched_vacancies': searched_vacancies,
                                                                       'companies': companies,
                                                                       'vacancies_count': vacancies_count})
            else:
                return redirect('/')


class SpecVacancies(View):

    def get(self, request, cat_id):

        speca = Specialty.objects.get(id=cat_id)
        spec_vacan = Vacancy.objects.filter(specialty_id=cat_id)
        vacancies_amount = len(spec_vacan)
        companies = Company.objects.all()
        return render(request, 'jumanji/spec_vacancies.html',
                      context={'spec_vacan': spec_vacan,
                               'speca': speca,
                               'companies': companies,
                               'vacancies_amount': vacancies_amount})


class CompanyCard(View):

    def get(self, request, com_id):

        compa = Company.objects.get(id=com_id)
        vacan_of_company = Vacancy.objects.filter(company_id=com_id)
        vacancies_amount = len(vacan_of_company)
        return render(request, 'jumanji/company.html',
                      context={'compa': compa,
                               'vacan_of_company': vacan_of_company,
                               'vacancies_amount': vacancies_amount})


class OneVacancy(View):

    def get(self, request, vac_id):

        one_vac = Vacancy.objects.get(id=vac_id)
        compa_of_one_vac = Company.objects.get(id=one_vac.company_id)
        return render(request, 'jumanji/vacancy.html',
                      context={'one_vac': one_vac,
                               'compa_of_one_vac': compa_of_one_vac})


class SendApply(View):

    def post(self, request, vac_id):

        if request.method == 'POST':
            vacancy = Vacancy.objects.get(id=vac_id)
            owner = Company.objects.get(id=vacancy.company_id)
            user = get_user_model().objects.get(id=owner.owner_id)
            send_form = SendForm(request.POST)
            if send_form.is_valid():
                data = send_form.cleaned_data
                Application.objects.create(written_username=data['name'],
                                           written_phone=data['telephone'],
                                           written_cover_letter=data['cover_letter'],
                                           vacancy=vacancy,
                                           user=user)
                return render(request, 'jumanji/sent.html', context={'vacancy': vacancy})
            else:
                return redirect(reverse('choice_vac'))


class OwnCompanyCreate(View):

    def get(self, request):

        return render(request, 'jumanji/company-edit.html')

    def post(self, request):

        if request.method == 'POST':
            create_company = EditOwnCompany(request.POST, request.FILES)
            if create_company.is_valid():
                data = create_company.cleaned_data
                Company.objects.create(title=data['title'],
                                       description=data['description'],
                                       employee_count=data['employee_count'],
                                       location=data['location'],
                                       logo=data['logo'],
                                       owner=request.user)
                return redirect(reverse('own-company-edit'))
            else:
                print(create_company.errors)
                return render(request, 'jumanji/company-edit.html')


class OwnCompanyEdit(View):

    def get(self, request):

        own_company = Company.objects.filter(owner=request.user).first()
        if own_company is None:
            return redirect(reverse('own-company-create'))
        else:
            return render(request, 'jumanji/company-edit.html', context={'own_company': own_company})

    def post(self, request):

        if request.method == 'POST':
            own_company = Company.objects.get(owner=request.user)
            edit_company = EditOwnCompany(request.POST, request.FILES, instance=own_company)
            if edit_company.is_valid():
                edit_company.save()
                return render(request, 'jumanji/company-edit.html', context={'own_company': own_company})
            else:
                return render(request, 'jumanji/company-edit.html')


class OwnResumeCreateButton(View):

    def get(self, request):

        resume = Resume.objects.filter(user_id=request.user).first()
        if resume is None:
            return render(request, 'jumanji/resume-create.html')
        else:
            return redirect(reverse('own-resume-edit'))


class OwnResumeCreate(View):

    def get(self, request):

        specialities = Specialty.objects.all()
        return render(request, 'jumanji/resume-edit.html', context={'specialities': specialities})

    def post(self, request):
        if request.method == 'POST':
            create_resume = ResumeForm(request.POST)
            if create_resume.is_valid():
                data = create_resume.cleaned_data
                Resume.objects.create(name=data['name'],
                                      surname=data['surname'],
                                      status=data['status'],
                                      salary=data['salary'],
                                      specialty=data['specialty'],
                                      qualification=data['qualification'],
                                      education=data['education'],
                                      experience=data['experience'],
                                      portfolio=data['portfolio'],
                                      user=request.user)
                return redirect(reverse('own-resume-edit'))
            else:
                return render(request, 'jumanji/resume-edit.html')


class OwnResumeEdit(View):

    def get(self, request):

        resume = Resume.objects.filter(user_id=request.user).first()
        specialities = Specialty.objects.all()
        if resume is not None:
            return render(request, 'jumanji/resume-edit.html', context={'resume': resume,
                                                                        'specialities': specialities})

    def post(self, request):

        if request.method == 'POST':
            specialities = Specialty.objects.all()
            resume = Resume.objects.get(user=request.user)
            edit_resume = ResumeForm(request.POST, instance=resume)
            if edit_resume.is_valid():
                edit_resume.save()
                return render(request, 'jumanji/resume-edit.html', context={'resume': resume,
                                                                            'specialities': specialities})
            else:
                return render(request, 'jumanji/resume-edit.html')


class OwnCompanyVacanciesButton(View):

    def get(self, request):

        company = Company.objects.filter(owner=request.user).first()
        if company is None:
            return redirect(reverse('own-company-create'))
        else:
            vacancies = Vacancy.objects.filter(company=company).annotate(applications_count=Count('applications'))
            if vacancies is None:
                return redirect(reverse('create-vacancy'))
            else:
                return render(request, 'jumanji/vacancy-list.html', context={'vacancies': vacancies})


class OwnCompanyVacancyCreate(View):

    def get(self, request):

        specialities = Specialty.objects.all()
        return render(request, 'jumanji/vacancy-edit.html', context={'specialities': specialities})

    def post(self, request):

        if request.method == 'POST':
            create_vacancy = VacancyForm(request.POST)
            if create_vacancy.is_valid():
                data = create_vacancy.cleaned_data
                Vacancy.objects.create(title=data['title'],
                                       salary_min=data['salary_min'],
                                       salary_max=data['salary_max'],
                                       description=data['description'],
                                       skills=data['skills'],
                                       specialty=data['specialty'],
                                       company=request.user.company
                                       )
                return redirect(reverse('vacancies-suggest'))
            else:
                return redirect(reverse('create-vacancy'))


class OwnCompanyVacancyEdit(View):

    def get(self, request, vacancy_id):

        specialities = Specialty.objects.all()
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        applications = Application.objects.filter(vacancy_id=vacancy.id)
        amount_applications = len(applications)
        if vacancy is not None:
            return render(request, 'jumanji/vacancy-edit.html', context={'vacancy': vacancy,
                                                                         'applications': applications,
                                                                         'specialities': specialities,
                                                                         'amount_applications': amount_applications})
        else:
            return redirect(reverse('create-vacancy'))

    def post(self, request, vacancy_id):

        if request.method == 'POST':
            specialities = Specialty.objects.all()
            vacancy = Vacancy.objects.get(id=vacancy_id)
            applications = Application.objects.filter(vacancy_id=vacancy.id)
            edit_vacancy = VacancyForm(request.POST, instance=vacancy)
            if edit_vacancy.is_valid():
                edit_vacancy.save()
                return render(request, 'jumanji/vacancy-edit.html', context={'vacancy': vacancy,
                                                                             'applications': applications,
                                                                             'specialities': specialities})
            else:
                return redirect(reverse('edit-vacancy'))
