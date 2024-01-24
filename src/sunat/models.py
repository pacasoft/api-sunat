from django.db import models


class DNI(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=8, db_index=True)
    nombres = models.CharField(max_length=200)
    apellido_paterno = models.CharField(max_length=200)
    apellido_materno = models.CharField(max_length=200)
    ubigeo = models.CharField(max_length=200, blank=True, null=True)

    provincia = models.CharField(max_length=200, blank=True, null=True)
    departamento = models.CharField(max_length=200, blank=True, null=True)
    distrito = models.CharField(max_length=200, blank=True, null=True)

    direccion = models.TextField(blank=True, null=True, default="-")

    def __str__(self):
        return str(self.numero) + ": " + self.apellido_paterno + " " + self.apellido_materno + ", " + self.nombres

    class Meta:
        verbose_name_plural = "DNIs"
        ordering = ['numero']


class RUC(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=11, db_index=True)
    razon_social = models.CharField(max_length=200)

    estado_contribuyente = models.CharField(max_length=200)
    condicion_domicilio = models.CharField(max_length=200)

    direccion = models.TextField(blank=True, null=True)
    ubigeo = models.CharField(max_length=200, blank=True, null=True)
    departamento = models.CharField(max_length=200, blank=True, null=True)
    provincia = models.CharField(max_length=200, blank=True, null=True)
    distrito = models.CharField(max_length=200, blank=True, null=True)

    tipo_via = models.CharField(max_length=200, blank=True, null=True)
    nombre_via = models.CharField(max_length=200, blank=True, null=True)
    codigo_zona = models.CharField(max_length=200, blank=True, null=True)
    tipo_zona = models.CharField(max_length=200, blank=True, null=True)
    numero_dir = models.CharField(max_length=200, blank=True, null=True)
    interior = models.CharField(max_length=200, blank=True, null=True)
    lote = models.CharField(max_length=200, blank=True, null=True)
    departamento = models.CharField(max_length=200, blank=True, null=True)
    manzana = models.CharField(max_length=200, blank=True, null=True)
    kilometro = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.numero) + ": " + self.razon_social

    class Meta:
        verbose_name_plural = "RUCs"
        ordering = ['numero']
        


# TODO: Crear modelos para el ubigeo (departamento, provincia, distrito)
