from sunat.models import RUC, DNI
from sunat.serializers import RUCSerializer, DNISerializer
from rest_framework.exceptions import NotFound, APIException
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


# docs: https://www.django-rest-framework.org/api-guide/generic-views/#retrieveapiview
#       https://medium.com/the-andela-way/creating-a-djangorest-api-using-djangorestframework-part-2-1231fe949795
#       https://andela.com/blog-posts/how-to-use-django-rest-framework-apiview-to-create-a-django-api-part-2

# To do:
#    clean temporal files


# Python
class export_to_sqlite(APIView):
    def get(self, request):
        try:
            from sunat.extract_padron import ExtractPadron
            extractPadron = ExtractPadron()
            return extractPadron.export_to_sqlite()
        except Exception as e:
            print('Error in export_to_sqlite:', e)
            return Response({
                "statusCode": 400,
                "body": {
                    "errors": [
                        {
                            "message": "error en los datos ingresados"
                        }
                    ]
                }
            })


class DNIDetail(generics.RetrieveAPIView):
    queryset = DNI.objects.all()
    serializer_class = DNISerializer
    lookup_field = 'numero'

    def get_object(self):
        try:
            numero = self.kwargs['numero']  # get the DNI from the URL
            return super().get_object()
        except Http404:
            print("DNI not found:", numero)

            raise NotFound({
                "statusCode": 404,
                "body": {
                    "errors": [
                        {
                            "message": "El DNI ("+numero+") ingresado no existe o no es válido"
                        }
                    ]
                }
            })
        except Exception as e:
            print("Error: ", e)
            raise APIException({
                "statusCode": 400,
                "body": {
                    "errors": [
                        {
                            "message": "error en los datos ingresados"
                        }
                    ]
                }
            })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "statusCode": 200,
            "body": serializer.data
        })


class RUCDetail(generics.RetrieveAPIView):
    queryset = RUC.objects.all()
    serializer_class = RUCSerializer
    lookup_field = 'numero'

    def get_object(self):
        try:
            numero = self.kwargs['numero']  # get the DNI from the URL
            return super().get_object()
        except Http404:
            print("RUC not found:", numero)

            raise NotFound({
                "statusCode": 404,
                "body": {
                    "errors": [
                        {
                            "message": f"El RUC ({numero}) ingresado no existe o no es válido"
                        }
                    ]
                }
            })
        except Exception as e:
            print("Error: ", e)
            raise APIException({
                "statusCode": 400,
                "body": {
                    "errors": [
                        {
                            "message": "error en los datos ingresados"
                        }
                    ]
                }
            })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer = serializer.data
        # serializer["id"] = serializer["id"]
        return Response({
            "statusCode": 200,
            "body": serializer
        })


# EXAMPLES FROM SUNAT.DEV
# BAD RUC: NO EXISTE
# {
#     "statusCode": 404,
#     "body": {
#         "errors": [
#             {
#             "message": "El RUC ingresado no existe o no es válido"
#             }
#         ]
#     },
#     "url-de-consulta": "https://api.sunat.dev/ruc/10712759768?apikey=7tsRb3To4HDxHOcmoPRXRMBZvRsFNdV0XdydnKgqJnsYhuh6Bg1ENv4hEOUXifac"
# }
# BAD RUC: ERROR DE CLIENTE
# {
#     "statusCode": 400,
#     "body": {
#         "errors": [
#             {
#             "message": "error en los datos ingresados -> 107127597695"
#             }
#         ]
#     },
#     "url-de-consulta": "https://api.sunat.dev/ruc/107127597695?apikey=7tsRb3To4HDxHOcmoPRXRMBZvRsFNdV0XdydnKgqJnsYhuh6Bg1ENv4hEOUXifac"
# }
# GOOD RUC:
# {
#     "statusCode": 200,
#     "body": {
#         "numeroRuc": "10712759769",
#         "datosContribuyente": {
#             "desRazonSocial": "LOPEZ CRUZ ISRAEL SANTIAGO",
#             "desNomApe": "ISRAEL SANTIAGO LOPEZ CRUZ",
#             "ubigeo": {
#                 "codUbigeo": "180301",
#                 "desDistrito": "ILO",
#                 "desProvincia": "ILO ",
#                 "desDepartamento": "MOQUEGUA "
#             },
#             "desDireccion": "MZA. C LOTE. 14 CIUDAD DEL PESCADOR",
#             "codEstado": "ACTIVO",
#             "codDomHabido": "HABIDO"
#         }
#     },
#     "url-de-consulta": "https://api.sunat.dev/ruc/10712759769?apikey=7tsRb3To4HDxHOcmoPRXRMBZvRsFNdV0XdydnKgqJnsYhuh6Bg1ENv4hEOUXifac"
# }
