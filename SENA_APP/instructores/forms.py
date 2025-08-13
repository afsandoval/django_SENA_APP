from django import forms
from .models import Instructor

class InstructorForm(forms.Form):
    documento_identidad = forms.CharField(max_length=20, label="Documento de Identidad", help_text="Ingrese el número de documento de identidad del instructor.")
    tipo_documento = forms.ChoiceField(choices=Instructor.TIPO_DOCUMENTO_CHOICES, label="Tipo de Documento", help_text="Seleccione el tipo de documento del instructor.")
    nombre = forms.CharField(max_length=100, label="Nombre", help_text="Ingrese el nombre del instructor.")
    apellido = forms.CharField(max_length=100, label="Apellido", help_text="Ingrese el apellido del instructor.")
    telefono = forms.CharField(max_length=10, required=False, label="Teléfono", help_text="Ingrese el número de teléfono del instructor.")
    correo = forms.EmailField(required=False, label="Correo Electrónico", help_text="Ingrese el correo electrónico del instructor.")
    fecha_nacimiento = forms.DateField(label="Fecha de Nacimiento", help_text="Ingrese la fecha de nacimiento del instructor.")
    ciudad = forms.CharField(max_length=100, required=False, label="Ciudad", help_text="Ingrese la ciudad de residencia del instructor.")
    direccion = forms.CharField(widget=forms.Textarea, required=False, label="Dirección", help_text="Ingrese la dirección del instructor.")
    nivel_educativo = forms.ChoiceField(choices=Instructor.NIVEL_EDUCATIVO_CHOICES, label="Nivel Educativo", help_text="Seleccione el nivel educativo del instructor.")
    especialidad = forms.CharField(max_length=100, label="Especialidad", help_text="Ingrese la especialidad del instructor.")
    anos_experiencia = forms.IntegerField(min_value=0, label="Años de Experiencia", help_text="Ingrese los años de experiencia del instructor.")
    activo = forms.BooleanField(required=False, initial=True, label="Activo", help_text="Indique si el instructor está activo.")
    fecha_vinculacion = forms.DateField(label="Fecha de Vinculación", help_text="Ingrese la fecha de vinculación del instructor.")
    fecha_registro = forms.DateField(label="Fecha de Registro", help_text="Ingrese la fecha de registro del instructor.")

    def clean(self):
        cleaned_data = super().clean()
        documento = cleaned_data.get('documento_identidad')
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')

        if not documento or not nombre or not apellido:
            raise forms.ValidationError("Todos los campos son obligatorios.")

        return cleaned_data

    def clean_documento_identidad(self):
        documento = self.cleaned_data['documento_identidad']
        if not documento.isdigit():
            raise forms.ValidationError("El documento debe contener solo números.")
        return documento
        
        
    def save(self):
        """Método para guardar el instructor en la base de datos"""
        try:
            instructor = Instructor.objects.create(
                documento_identidad=self.cleaned_data['documento_identidad'],
                tipo_documento=self.cleaned_data['tipo_documento'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                telefono=self.cleaned_data.get('telefono', ''),
                correo=self.cleaned_data.get('correo', ''),
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                ciudad=self.cleaned_data.get('ciudad', ''),
                direccion=self.cleaned_data.get('direccion', ''),
                nivel_educativo=self.cleaned_data['nivel_educativo'],
                especialidad=self.cleaned_data['especialidad'],
                anos_experiencia=self.cleaned_data['anos_experiencia'],
                activo=self.cleaned_data.get('activo', True),
                fecha_vinculacion=self.cleaned_data['fecha_vinculacion'],
                fecha_registro=self.cleaned_data['fecha_registro']
            )
            return instructor
        except Exception as e:
            raise forms.ValidationError(f"Error al crear el instructor: {str(e)}")