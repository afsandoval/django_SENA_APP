from django.http import HttpResponse
from django.template import loader
from .models import Aprendiz
# Create your views here.

def aprendices(request):
    lista_aprendices = Aprendiz.objects.all().order_by('apellido', 'nombre')
    template = loader.get_template('lista_aprendices.html')
    context = {
    'lista_aprendices': lista_aprendices,
    'total_aprendices': lista_aprendices.count(),
    }
    return HttpResponse(template.render(context, request))

def inicio(request):
    template = loader.get_template('inicio.html')
    return HttpResponse(template.render())