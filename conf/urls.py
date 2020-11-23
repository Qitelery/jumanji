"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jumanji.views import MainView, ListVacancies, SpecVacancies, CompanyCard, OneVacancy, SendApply, \
    RegistrationPost, LogIn, LogOut, Search, OwnCompanyEdit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='juman'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('register/', RegistrationPost.as_view(), name='register'),
    path('search/', Search.as_view(), name='search'),
    path('vacancies/', ListVacancies.as_view(), name='all_vacancies'),
    path('vacancies/cat/<int:cat_id>/', SpecVacancies.as_view(), name='spec_vac'),
    path('companies/<int:com_id>/', CompanyCard.as_view(), name='card_of_company'),
    path('vacancies/<int:vac_id>/', OneVacancy.as_view(), name='choice_vac'),
    path('vacancies/<int:vac_id>/sent/', SendApply.as_view()),
    path('company-edit/', OwnCompanyEdit.as_view(), name='own-company')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
