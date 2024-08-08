from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Empresas, Documentos, Metricas

# Create your views here.


def add_company(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')

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


def list_companies(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')

    if request.method == 'GET':
        companies = Empresas.objects.filter(user=request.user)
        return render(
            request,
            'list_companies.html',
            {'companies': companies}
        )

def company(request, id):
    company = Empresas.objects.get(id=id)

    if company.user != request.user:
        messages.add_message(
            request,
            messages.WARNING,
            f'Você não tem permissão para cadastrar '
            f'documentos na empresa: {company.name}!'
        )
        return redirect(f'/companies/list_companies')

    if request.method == 'GET':
        documents = Documentos.objects.filter(company=company)
        return render(request, 'company.html', {
            'company': company,
            'documents': documents
        })

def add_document(request, id):
    if request.method == 'POST':
        company = Empresas.objects.get(id=id)
        title = request.POST['title']
        file = request.FILES.get('file')

        if company.user != request.user:
            messages.add_message(
                request,
                messages.WARNING,
                f'Você não tem permissão para cadastrar '
                f'documentos na empresa: {company.name}!'
            )
            return redirect(f'/companies/list_companies')

        if title == '':
            messages.add_message(
                request,
                messages.WARNING,
                'Título é obrigatório!'
            )
            return redirect(f'/companies/company/{id}')

        if not file:
            messages.add_message(
                request,
                messages.WARNING,
                'Escolha um arquivo!'
            )
            return redirect(f'/companies/company/{id}')

        if not file.name.endswith('.pdf'):
            messages.add_message(
                request,
                messages.WARNING,
                'O arquivo tem que ser um PDF!'
            )
            return redirect(f'/companies/company/{id}')

        document = Documentos(
            company=company,
            title=title,
            file=file
        )

        document.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Arquivo cadastrado com sucesso!'
        )

        return redirect(f'/companies/company/{id}')


def remove_document(request, id):
    document = Documentos.objects.get(id=id)

    if document.company.user != request.user:
        messages.add_message(
            request,
            messages.WARNING,
            f'Você não tem permissão para remover '
            f'documentos na empresa: {company.name}!'
        )

    document.delete()

    messages.add_message(
        request,
        messages.SUCCESS,
        'Documento removido com sucesso!'
    )
    return redirect(f'/companies/company/{document.company.id}')


def add_metric(request, id):
    company = Empresas.objects.get(id=id)
    title = request.POST['title2']
    value = request.POST['value']

    metric = Metricas(
        company=company,
        title=title,
        value=value
    )

    metric.save()

    messages.add_message(
        request,
        messages.SUCCESS,
        "Métrica cadastrada com sucesso"
    )

    return redirect(f'/companies/company/{company.id}')