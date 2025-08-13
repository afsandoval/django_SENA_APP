from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from .models import Instructor
from django.shortcuts import get_object_or_404

from instructores.forms import InstructorForm
from django.views import generic
from django.contrib import messages
from django.views.generic import FormView



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


class InstructorFormView(FormView):
    template_name = 'crear_instructor.html'
    form_class = InstructorForm
    success_url = "../instructores/"

    def form_valid(self, form):
        # Guardar el instructor
        instructor = form.save()
        
        # Agregar mensaje de éxito
        messages.success(
            self.request, 
            f'El instructor {instructor.nombre} {instructor.apellido} ha sido registrado exitosamente.'
        )
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 
            'Por favor, corrija los errores en el formulario.'
        )
        return super().form_invalid(form)

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import InstructorForm
# from .models import Instructor

# def crear_instructor(request):
#     """Vista para crear un nuevo instructor"""
#     if request.method == 'POST':
#         form = InstructorForm(request.POST)
#         if form.is_valid():
#             try:
#                 instructor = form.save()
#                 messages.success(
#                     request, 
#                     f'El instructor {instructor.nombre} {instructor.apellido} ha sido registrado exitosamente.'
#                 )
#                 return redirect('lista_instructores')  # Cambia por tu URL de lista
#             except Exception as e:
#                 messages.error(request, f'Error al guardar el instructor: {str(e)}')
#         else:
#             messages.error(request, 'Por favor, corrija los errores en el formulario.')
#             # Para depuración, imprime los errores
#             print("Errores del formulario:", form.errors)
#     else:
#         form = InstructorForm()
    
#     return render(request, 'crear_instructor.html', {
#         'form': form,
#         'titulo': 'Registrar Nuevo Instructor'
#     })
    
    