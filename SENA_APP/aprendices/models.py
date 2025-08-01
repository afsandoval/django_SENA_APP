from django.db import models

# Create your models here.
class Aprendiz(models.Model):
    documento_identidad = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, null=True)
    correo = models.EmailField(null=True)
    fecha_nacimiento = models.DateField()
    ciudad = models.CharField(max_length=100, null=True)
    # programa = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Aprendiz"
        verbose_name_plural = "Aprendices"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.documento_identidad}"

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Curso(models.Model):
    ESTADO_CHOICES = [
        ('PRO', 'Programado'),
        ('INI', 'Iniciado'),
        ('EJE', 'En Ejecución'),
        ('FIN', 'Finalizado'),
        ('CAN', 'Cancelado'),
        ('SUS', 'Suspendido'),
    ]

    codigo = models.CharField(max_length=30,unique=True,verbose_name="Código del Curso")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Curso")
    programa = models.ForeignKey('programas.Programa', on_delete=models.CASCADE, verbose_name="Programa de Formación")
    instructor_coordinador = models.ForeignKey('instructores.Instructor', on_delete=models.CASCADE, related_name='cursos_coordinados', verbose_name="Instructor Coordinador")
    instructores = models.ManyToManyField('instructores.Instructor', through='InstructorCurso', related_name='cursos_impartidos', verbose_name="Instructores")
    aprendices = models.ManyToManyField(Aprendiz, through='AprendizCurso', related_name='cursos', verbose_name="Aprendices")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Finalización")
    horario = models.CharField(max_length=100, verbose_name="Horario")
    aula = models.CharField(max_length=50, verbose_name="Aula/Ambiente")
    cupos_maximos = models.PositiveIntegerField(verbose_name="Cupos Máximos")
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='PRO', verbose_name="Estado del Curso")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def cupos_disponibles(self):
        return self.cupos_maximos - self.aprendices.count()

    def porcentaje_ocupacion(self):
        if self.cupos_maximos > 0:
            return (self.aprendices.count() / self.cupos_maximos) * 100
        return 0


class InstructorCurso(models.Model):
    instructor = models.ForeignKey('instructores.Instructor', on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100, verbose_name="Rol en el Curso")
    fecha_asignacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Asignación")

    class Meta:
        verbose_name = "Instructor por Curso"
        verbose_name_plural = "Instructores por Curso"
        unique_together = ['instructor', 'curso']

    def __str__(self):
        return f"{self.instructor} - {self.curso} ({self.rol})"


class AprendizCurso(models.Model):
    ESTADO_CHOICES = [
        ('INS', 'Inscrito'),
        ('ACT', 'Activo'),
        ('DES', 'Desertor'),
        ('GRA', 'Graduado'),
        ('SUS', 'Suspendido'),
    ]

    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True, verbose_name="Fecha de Inscripción")
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='INS', verbose_name="Estado en el Curso")
    nota_final = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, verbose_name="Nota Final")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Aprendiz por Curso"
        verbose_name_plural = "Aprendices por Curso"
        unique_together = ['aprendiz', 'curso']

    def __str__(self):
        return f"{self.aprendiz} - {self.curso} ({self.estado})"