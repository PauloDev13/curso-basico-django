from django.shortcuts import render
from company.models import Empresas

# Create your views here.


def suggestion(request):
    areas = Empresas.area_choices

    if request.method == 'GET':
        return render(request, 'suggestion.html', {
            'areas': areas,
        })
    elif request.method == 'POST':
        investor_type = request.POST['investor_type']
        area = request.POST.getlist('area')
        value = request.POST['value']

        if investor_type == 'C':
            companies = (
                Empresas.objects
                .filter(time_existence='+5')
                .filter(estagio='E')
            )
        elif investor_type == 'D':
            companies = (
                Empresas.objects
                .filter(time_existence__in=['-6', '+6', '+1'])
                .exclude(estagio='E')
            )

        companies = companies.filter(area__in=area)

        selected_companies = []

        for company in companies:
            percentage = float(value) * 100 / float(company.valuation)

            if percentage > 1:
                selected_companies.append(company)

        return render(request, 'suggestion.html', {
            'areas': areas,
            'companies': selected_companies,
        })

