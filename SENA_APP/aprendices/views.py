from django.http import HttpResponse
from django.template import loader
from .models import Aprendiz, Curso
from django.shortcuts import get_object_or_404
from instructores.models import Instructor
from programas.models import Programa

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
    # Estadísticas generales
    total_aprendices = Aprendiz.objects.count()
    total_instructores = Instructor.objects.count() 
    total_programas = Programa.objects.count()
    total_cursos = Curso.objects.count()
    cursos_activos = Curso.objects.filter(estado__in=['INI', 'EJE']).count()
    template = loader.get_template('inicio.html')
    
    context = {
        'total_aprendices': total_aprendices,
        'total_cursos': total_cursos,
        'cursos_activos': cursos_activos,
        'total_instructores': total_instructores,
        'total_programas': total_programas,
    }
    
    return HttpResponse(template.render(context, request))


def lista_cursos(request):
    cursos = Curso.objects.all().order_by('-fecha_inicio')
    template = loader.get_template('lista_cursos.html')
    
    context = {
        'lista_cursos': cursos,
        'total_cursos': cursos.count(),
        'titulo': 'Lista de Cursos'
    }
    
    return HttpResponse(template.render(context, request))

def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    aprendices_curso = curso.aprendizcurso_set.all()
    instructores_curso = curso.instructorcurso_set.all()
    template = loader.get_template('detalle_curso.html')
    
    context = {
        'curso': curso,
        'aprendices_curso': aprendices_curso,
        'instructores_curso': instructores_curso,
    }
    
    return HttpResponse(template.render(context, request))

def detalle_aprendiz(request, aprendiz_id):
    aprendiz = get_object_or_404(Aprendiz, id=aprendiz_id)
    template = loader.get_template('detalle_aprendiz.html')
    
    context = {
        'aprendiz': aprendiz,
    }
    
    return HttpResponse(template.render(context, request))