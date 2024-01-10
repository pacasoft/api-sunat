
from rest_framework import serializers
from sunat.models import RUC, DNI


class DNISerializer(serializers.ModelSerializer):
    class Meta:
        model = DNI
        fields = (
            'numero',
            'nombres',
            'apellido_paterno',
            'apellido_materno',
            'ubigeo',
            'provincia',
            'departamento',
            'distrito',
            'direccion',
        )


class RUCSerializer(serializers.ModelSerializer):
    class Meta:
        model = RUC
        fields = (
            'numero',
            'razon_social',
            'estado_contribuyente',
            'condicion_domicilio',
            'direccion',
            'ubigeo',
            'departamento',
            'provincia',
            'distrito',
        )
