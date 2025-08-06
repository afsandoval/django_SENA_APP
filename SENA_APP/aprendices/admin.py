from django.contrib import admin
from .models import Aprendiz, Curso, InstructorCurso, AprendizCurso

# Aprendiz Admin (actualizado)
@admin.register(Aprendiz)
class AprendizAdmin(admin.ModelAdmin):
    list_display = [
        'documento_identidad', 
        'nombre_completo', 
        'correo', 
        'telefono', 
        'ciudad'
    ]
    list_filter = ['ciudad']
    search_fields = [
        'documento_identidad', 
        'nombre', 
        'apellido', 
        'correo'
    ]
    list_per_page = 20
    ordering = ['apellido', 'nombre']
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'documento_identidad', 
                'nombre', 
                'apellido', 
                'fecha_nacimiento'
            )
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'correo', 'ciudad')
        }),
    )

    def nombre_completo(self, obj):
        return obj.nombre_completo()
    nombre_completo.short_description = 'Nombre Completo'


# Inlines para el admin de Cursos: Los inlines permiten editar modelos relacionados dentro del formulario del modelo principal. 
# Es como tener "mini-formularios" integrados.
class InstructorCursoInline(admin.TabularInline):
    model = InstructorCurso # ← Modelo de la tabla intermedia
    extra = 1 # ← Cuántas filas vacías mostrar por defecto
    fields = ['instructor', 'rol'] # ← Campos a mostrar en el inline


class AprendizCursoInline(admin.TabularInline):
    model = AprendizCurso
    extra = 0 # ← No mostrar filas vacías
    fields = ['aprendiz', 'estado', 'nota_final', 'observaciones']


# Admin principal de Cursos
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'nombre',
        'programa',
        'instructor_coordinador',
        'fecha_inicio',
        'fecha_fin',
        'estado',
        'cupos_info'
    ]
    list_filter = [
        'estado',
        'programa__nivel_formacion',
        'fecha_inicio',
        'programa'
    ]
    search_fields = [
        'codigo',
        'nombre',
        'programa__nombre',
        'instructor_coordinador__nombre',
        'instructor_coordinador__apellido'
    ]
    list_per_page = 15
    ordering = ['-fecha_inicio']
    date_hierarchy = 'fecha_inicio'
    
    inlines = [InstructorCursoInline, AprendizCursoInline]

    fieldsets = (
        ('Información Básica', {
            'fields': (
                ('codigo', 'nombre'),
                'programa',
                'instructor_coordinador'
            )
        }),
        ('Fechas y Horarios', {
            'fields': (
                ('fecha_inicio', 'fecha_fin'),
                'horario',
                'aula'
            )
        }),
        ('Configuración', {
            'fields': (
                'cupos_maximos',
                'estado',
                'observaciones'
            )
        }),
    )

    def cupos_info(self, obj):
        ocupados = obj.aprendices.count()
        disponibles = obj.cupos_disponibles()
        porcentaje = obj.porcentaje_ocupacion()
        return f"{ocupados}/{obj.cupos_maximos} ({porcentaje:.1f}%)"
    cupos_info.short_description = 'Ocupación'


# Admin para las relaciones
@admin.register(InstructorCurso)
class InstructorCursoAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'curso', 'rol', 'fecha_asignacion']
    list_filter = ['rol', 'fecha_asignacion']
    search_fields = [
        'instructor__nombre',
        'instructor__apellido',
        'curso__nombre',
        'curso__codigo'
    ]


@admin.register(AprendizCurso)
class AprendizCursoAdmin(admin.ModelAdmin):
    list_display = [
        'aprendiz',
        'curso',
        'estado',
        'nota_final',
        'fecha_inscripcion'
    ]
    list_filter = ['estado', 'fecha_inscripcion']
    search_fields = [
        'aprendiz__nombre',
        'aprendiz__apellido',
        'aprendiz__documento_identidad',
        'curso__nombre',
        'curso__codigo'
    ]
    list_editable = ['estado', 'nota_final']