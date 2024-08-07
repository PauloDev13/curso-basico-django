from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Empresas


# Create your views here.


def add_company(request):
    if request.method == 'GET':
        return render(request, 'add_company.html', {
            'time_existence': Empresas.time_existence_choices,
            'areas': Empresas.area_choices,
        })
    elif request.method == 'POST':
        try:
            name = request.POST['name']
            cnpj = request.POST['cnpj']
            site = request.POST['site']
            time_existence = request.POST['time_existence']
            description = request.POST['description']
            final_capture_date = request.POST['final_capture_date']
            percentual_equity = request.POST['percentual_equity']
            estagio = request.POST['estagio']
            area = request.POST['area']
            target_public = request.POST['target_public']
            price = request.POST['value']
            pitch = request.FILES.get('pitch')
            logo = request.FILES.get('logo')


            company = Empresas(
                user=request.user,
                name=name,
                cnpj=cnpj,
                site=site,
                time_existence=time_existence,
                description=description,
                final_capture_date=final_capture_date,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                target_public=target_public,
                value=price,
                pitch=pitch,
                logo=logo
            )

            company.save()
        except Exception as e:
            print(f'CAIU NO EXCEPT: {e}')
            messages.add_message(request, messages.ERROR, 'Erro ao cadastrar Empresa!')
            return redirect('/companies/add_company')

        messages.add_message(request, messages.SUCCESS, 'Empresa cadastrada com sucesso!')
        return redirect('/companies/add_company')
