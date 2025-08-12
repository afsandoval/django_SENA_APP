from django import forms
from .models import Aprendiz


class AprendizForm(forms.Form):
    documento_identidad = forms.CharField(max_length=20, label="Documento de Identidad", help_text="Ingrese el número de documento de identidad del aprendiz.")
    nombre = forms.CharField(max_length=100, label="Nombre", help_text="Ingrese el nombre del aprendiz.")
    apellido = forms.CharField(max_length=100, label="Apellido", help_text="Ingrese el apellido del aprendiz.")
    telefono = forms.CharField(max_length=10, label="Teléfono", help_text="Ingrese el número de teléfono del aprendiz.")
    correo = forms.EmailField(label="Correo Electrónico", help_text="Ingrese el correo electrónico del aprendiz.")
    fecha_nacimiento = forms.DateField(label="Fecha de Nacimiento", help_text="Ingrese la fecha de nacimiento del aprendiz.")
    ciudad = forms.CharField(max_length=100, required=False, label="Ciudad", help_text="Ingrese la ciudad de residencia del aprendiz.")
    
    
    #Validaciones personalizadas 
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

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono
    
    #Crear un método para guardar los datos del formulario en la base de datos
    def save(self):
        Aprendiz.objects.create(
            documento_identidad=self.cleaned_data['documento_identidad'],
            nombre=self.cleaned_data['nombre'],
            apellido=self.cleaned_data['apellido'],
            telefono=self.cleaned_data.get('telefono'),
            correo=self.cleaned_data.get('correo'),
            fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
            ciudad=self.cleaned_data.get('ciudad')
        )