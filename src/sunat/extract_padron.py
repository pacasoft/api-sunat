import pandas as pd
from rest_framework.response import Response
import time
import requests
from bs4 import BeautifulSoup
import zipfile
from sqlalchemy import create_engine, MetaData, Table, delete

import os
os.environ['OPENBLAS_NUM_THREADS'] = '4'


class ExtractPadron:
    def download_and_extract_padron(self):
        # return['padron_reducido.txt']
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
        os.remove(file_name)
        print('finished download_and_extract_padron')

        return unzipped_file

    def export_to_sqlite(self):
        try:
            print('started export_to_sqlite')
            
            file_name = self.download_and_extract_padron()
            table_name = 'sunat_ruc'

            mysql_connection_str  = 'mysql+pymysql://root:eduu@127.0.0.1:3306/mydb'
            engine = create_engine(mysql_connection_str)
            conn = engine.connect()

            metadata = MetaData()
            metadata.reflect(bind=engine)

            if table_name in metadata.tables:
                table = Table(table_name, metadata, autoload=True, autoload_with=engine)
                delete_query = delete(table)
                conn.execute(delete_query)
                print(f'{table_name} deleted')
            else:
                print(f'{table_name} not found')           

            conn.commit()
            conn.close()
            engine.dispose()    

            chunksize = 10 ** 6  # adjust this value depending on your available memory
            chunk_number = 1
            start_time = time.time()
            for chunk in pd.read_csv(file_name[0], delimiter='|', encoding='latin-1', on_bad_lines='warn',
                                     low_memory=False, chunksize=chunksize):
                engine = create_engine(mysql_connection_str)
                conn = engine.connect()
                metadata = MetaData()
                metadata.reflect(bind=engine)
                
                print("Readding chunk number:", chunk_number)
                chunk_number += 1
                chunk['Direccion'] = pd.concat([
                    chunk['TIPO DE VÍA'].astype(str),
                    chunk['NOMBRE DE VÍA'].astype(str),
                    chunk['MANZANA'].astype(str),
                    chunk['LOTE'].astype(str),
                    chunk['CÓDIGO DE ZONA'].astype(str),
                    chunk['TIPO DE ZONA'].astype(str),
                    chunk['NÚMERO'].astype(str),
                    chunk['INTERIOR'].astype(str)
                ], axis=1).apply(lambda row: ' '.join(row), axis=1)

                df_for_sql = chunk[
                    ['RUC', 'NOMBRE O RAZÓN SOCIAL', 'ESTADO DEL CONTRIBUYENTE', 'CONDICIÓN DE DOMICILIO', 'Direccion', 'UBIGEO',
                     'DEPARTAMENTO']]

                df_for_sql.columns = ['id', 'razon_social', 'estado_contribuyente', 'condicion_domicilio', 'direccion',
                                      'ubigeo', 'departamento']

                df_for_sql.to_sql("sunat_ruc", conn,
                                  if_exists='append', index=False)
                conn.commit()
                conn.close()
                print("Chunk number:", chunk_number, "completed in ",
                      time.time() - start_time, "seconds")
                start_time = time.time()

            os.remove(file_name)
            conn.commit()
            conn.close()
            engine.dispose()

            return Response({'message': 'Export to SQLite completed successfully'})

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
