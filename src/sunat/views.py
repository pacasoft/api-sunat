from rest_framework.response import Response
from rest_framework import generics

from django.http import Http404
from rest_framework.exceptions import NotFound, APIException

from sunat.serializers import RUCSerializer, DNISerializer
from sunat.models import RUC, DNI
from rest_framework.decorators import api_view

from django.http import HttpResponse
import requests
import zipfile
import pandas as pd
import os
from bs4 import BeautifulSoup

# docs: https://www.django-rest-framework.org/api-guide/generic-views/#retrieveapiview
#       https://medium.com/the-andela-way/creating-a-djangorest-api-using-djangorestframework-part-2-1231fe949795
#       https://andela.com/blog-posts/how-to-use-django-rest-framework-apiview-to-create-a-django-api-part-2

# To do:
#    clean temporal files


def download_and_extract_padron():
    print('started download_and_extract_padron')
    base_URL = "https://www.sunat.gob.pe/descargaPRR/"

    r = requests.get(base_URL + "mrc137_padron_reducido.html")
    r.content

    soup = BeautifulSoup(r.content, 'html.parser')

    # find the file_name
    link = soup.find('a', string='padrón_reducido_RUC.zip')['href']

    # get the file
    file = requests.get(link)
    open(link.split('/')[-1], 'wb').write(file.content)

    file_name = 'padron_reducido_ruc.zip'
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()
        unzipped_file = zip_ref.namelist()
    # os.remove(file_name)
    print('finished download_and_extract_padron')

    return unzipped_file


@api_view(['GET'])
def export_to_sqlite(request):
    '''
    RUC
    NOMBRE O RAZÓN SOCIAL
    ESTADO DEL CONTRIBUYENTE
    CONDICIÓN DE DOMICILIO
    UBIGEO
    *TIPO DE VÍA
    **NOMBRE DE VÍA
    *****CÓDIGO DE ZONA
    *******TIPO DE ZONA
    NÚMERO
    INTERIOR`
    ****LOTE
    DEPARTAMENTO
    ***MANZANA
    KILÓMETRO
    Direccion = tipo de via + nombre de via + mz + lt + codigo de zona + tipo de zona + numero + interior
    '''

    print('started export_to_sqlite')
    file_name = download_and_extract_padron()
    df = pd.read_csv(file_name[0], delimiter='|', encoding='latin-1', on_bad_lines='warn',
                     low_memory=False)
    # os.remove(file_name)

    df['Direccion'] = pd.concat([
        df['TIPO DE VÍA'].astype(str),
        df['NOMBRE DE VÍA'].astype(str),
        df['MANZANA'].astype(str),
        df['LOTE'].astype(str),
        df['CÓDIGO DE ZONA'].astype(str),
        df['TIPO DE ZONA'].astype(str),
        df['NÚMERO'].astype(str),
        df['INTERIOR'].astype(str)
    ], axis=1).apply(lambda row: ' '.join(row), axis=1)

    df_for_sql = df[
        ['RUC', 'NOMBRE O RAZÓN SOCIAL', 'ESTADO DEL CONTRIBUYENTE', 'CONDICIÓN DE DOMICILIO', 'Direccion', 'UBIGEO',
        'DEPARTAMENTO']]

    df_for_sql.columns = ['id', 'razon_social', 'estado_contribuyente', 'condicion_domicilio','direccion',
                        'ubigeo','departamento']

    conn = sqlite3.connect("db.sqlite3")
    df_for_sql.to_sql("sunat_ruc", conn, if_exists='append', index=False)
    sql_cur = conn.cursor()

    quer = sql_cur.execute("SELECT * FROM sunat_ruc LIMIT 5")
    rows = quer.fetchall()
    for row in rows:
        print(row)

    conn.close()
    return Response({'message': 'Export to SQLite completed successfully'})

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
        return Response({
            "statusCode": 200,
            "body": serializer.data
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
