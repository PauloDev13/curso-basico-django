from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db import models
from datetime import date


class Empresas(models.Model):
    time_existence_choices = (
        ('-6', 'Menos de 6 meses'),
        ('+6', 'Mais de 6 meses'),
        ('+1', 'Mais de 1 ano'),
        ('+5', 'Mais de 5 anos')

    )
    estagio_choices = (
        ('I', 'Tenho apenas uma idea'),
        ('MVP', 'Possuo um MVP'),
        ('MVPP', 'Possuo um MVP com clientes pagantes'),
        ('E', 'Empresa pronta para escalar'),
    )
    area_choices = (
        ('ED', 'Ed-tech'),
        ('FT', 'Fintech'),
        ('AT', 'Agrotech'),

    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=30)
    site = models.URLField()
    time_existence = models.CharField(
        max_length=2,
        choices=time_existence_choices,
        default='-6'
    )
    description = models.TextField()
    final_capture_date = models.DateField()
    percentual_equity = models.IntegerField()  # Percentual esperado
    estagio = models.CharField(
        max_length=4,
        choices=estagio_choices,
        default='I'
    )
    area = models.CharField(
        max_length=3,
        choices=area_choices
    )
    target_public = models.CharField(max_length=3)
    value = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )  # Valor total a ser vendido
    pitch = models.FileField(upload_to='pitchs')
    logo = models.FileField(upload_to='logo')

    def __str__(self):
        return f'{self.user.username} | {self.name}'

    @property
    def status(self):
        if date.today() > self.final_capture_date:
            return mark_safe('<span class="badge text-bg-success">Capitação finalizada</span>')
        return mark_safe('<span class="badge text-bg-primary">Em Capitação</span>')

    @property
    def valuation(self):
        return f'{(100 * self.value) / self.percentual_equity: .2f}'


class Documentos(models.Model):
    company = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='documentos')
    def __str__(self):
        return f'{self.title}'

class Metricas(models.Model):
    company = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=30)
    value = models.FloatField()

    def __str__(self):
        return self.title