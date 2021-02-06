from django.db import models

# Create your models here.
class Ciudad(models.Model):
    cod_ciudad = models.PositiveSmallIntegerField(primary_key=True, verbose_name='Código')
    descripcion = models.CharField(max_length=30, verbose_name='Ciudad')

    def __str__(self):
        return  "{0} ({1})".format(self.descripcion, self.cod_ciudad)

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        db_table = 'ciudad'

class Persona(models.Model):
    cod_persona = models.CharField(primary_key=True, max_length=8, verbose_name='Código')
    nombres = models.CharField(max_length=20, verbose_name='Nombres')
    apellidos = models.CharField(max_length=20, verbose_name='Apellidos')
    cedula = models.IntegerField()
    fecha_nac = models.DateField()
    direccion = models.CharField(max_length=100)
    tel_cel = models.CharField(max_length=12)
    email = models.EmailField(max_length=20)
    tipos_personas = [
        ('F', 'Fisica'),
        ('J', 'Juridica')
    ]
    tipo_persona = models.CharField(max_length=1, choices=tipos_personas, default='F')
    cod_ciudad = models.ForeignKey(Ciudad, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Código Ciudad')
    
    def __str__(self):
        return "{0} {1}".format(self.nombres, self.apellidos)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        db_table = 'persona'