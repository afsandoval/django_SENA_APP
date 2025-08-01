from django.http import HttpResponse
from django.template import loader
from .models import Instructor
from django.shortcuts import get_object_or_404

# Create your views here.

def instructores(request):
    lista_instructores = Instructor.objects.all().order_by('apellido', 'nombre')
    template = loader.get_template('lista_instructores.html')
    context = {
    'lista_instructores': lista_instructores,
    'total_instructores': lista_instructores.count(),
    }
    
    return HttpResponse(template.render(context, request))

def detalle_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    cursos_coordinados = instructor.cursos_coordinados.all()
    cursos_impartidos = instructor.cursos_impartidos.all()
    template = loader.get_template('detalle_instructor.html')
    
    context = {
        'instructor': instructor,
        'cursos_coordinados': cursos_coordinados,
        'cursos_impartidos': cursos_impartidos,
    }
    
    return HttpResponse(template.render(context, request))