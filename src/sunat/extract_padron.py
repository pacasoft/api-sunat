import logging
from rest_framework.response import Response
import time
import requests
from bs4 import BeautifulSoup
import zipfile
import sqlite3
from sunat.models import RUC
import os
# from sqlalchemy import create_engine, MetaData, Table
# from sqlalchemy.schema import drop


logging.basicConfig(filename='response.log', level=logging.INFO)


class ExtractPadron:
    def download_and_extract_padron(self):
        # return 'padron_reducido_ruc.txt'
        print('started download_and_extract_padron')
        base_URL = "https://www.sunat.gob.pe/descargaPRR/"

        r = requests.get(base_URL + "mrc137_padron_reducido.html")
        r.content

        soup = BeautifulSoup(r.content, 'html.parser')

        # find the file_name
        link = soup.find('a', string='padrón_reducido_RUC.zip')['href']

        # get the file
        file = requests.get(link)

        new_file_name = 'padron_reducido_ruc.zip'
        old_file_name = 'old_padron_reducido_ruc.zip'

        open(new_file_name, 'wb').write(file.content)

        if os.path.exists(old_file_name):
            # compare their sizes
            old_file_size = os.path.getsize(old_file_name)
            new_file_size = os.path.getsize(new_file_name)

            if old_file_size == new_file_size:
                print('El padron de ruc no ha cambiado...')
                return ['same_padron']
            else:
                print('El padron de ruc ha cambiado...')
                # os.rename(old_file_name, new_file_name)

        else:
            print('El padron de ruc ha cambiado...')

        file_name = 'padron_reducido_ruc.zip'
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall()
            unzipped_file = zip_ref.namelist()
        # os.remove(file_name)
        print('finished download_and_extract_padron')

        return unzipped_file[0]

    def extract_active_rucs(self, file_name):
        try:
            print('started extract_active_rucs')
            active_counter = 0
            non_active_counter = 0
            with open(file_name, 'r', encoding='ISO-8859-1') as file:
                with open('padron_reducido_ruc_activo.txt', 'w', encoding='ISO-8859-1') as activo_file:
                    # new file for non-activo lines
                    with open('padron_reducido_ruc_no_activo.txt', 'w', encoding='ISO-8859-1') as non_activo_file:
                        next(file)  # skip the first line
                        for line in file:

                            if 'ACTIVO' in line:
                                active_counter += 1
                                try:
                                    activo_file.write(line)
                                except Exception as e:
                                    print(
                                        f"An error occurred in line {active_counter+non_active_counter}: {str(e)}")
                                    logging.error(
                                        f"An error occurred in line {active_counter+non_active_counter}: {str(e)}")
                            else:
                                non_active_counter += 1
                                try:
                                    # write non-activo lines to the new file
                                    non_activo_file.write(line)
                                except Exception as e:
                                    print(
                                        f"An error occurred in line {active_counter+non_active_counter}: {str(e)}")
                                    logging.error(
                                        f"An error occurred in line {active_counter+non_active_counter}: {str(e)}")

            print("RUCs activos:", active_counter)
            logging.error("RUCs activos: " + active_counter)
            print("RUCs no activos:", non_active_counter)
            logging.error("RUCs no activos: " + non_active_counter)

        except FileNotFoundError:
            print(f"The file {file_name} does not exist.")
        except PermissionError:
            print(f"Permission denied to read the file {file_name}.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        print("Ended extract_active_rucs")
        logging.error("Ended extract_active_rucs")

    def add_to_database(self, file):
        try:
            start_time = time.time()
            data_list = []  # list of unsaved objects

            chunksize = 10 ** 6  # adjust this value depending on your available memory
            chunk_number = 1
            counter = 0
            for line in file:
                counter += 1

                try:
                    # RUC|NOMBRE O RAZ�N SOCIAL|ESTADO DEL CONTRIBUYENTE|CONDICI�N DE DOMICILIO|UBIGEO|TIPO DE V�A|NOMBRE DE V�A|C�DIGO DE ZONA|TIPO DE ZONA|N�MERO|INTERIOR|LOTE|DEPARTAMENTO|MANZANA|KIL�METRO|
                    data = line.split('|')
                    # Indexes of the fields in the array
                    indexes = [5, 6, 13, 11, 7, 8, 9, 10]

                    direccion = ' '.join([str(data[i])
                                          for i in indexes if data[i] != "-"])
                    data = {
                        'numero': data[0],
                        'razon_social': data[1],
                        'estado_contribuyente': data[2],
                        'condicion_domicilio': data[3],
                        'direccion': direccion,
                        'ubigeo': data[4],
                        'departamento': data[12],
                    }
                    data_list.append(RUC(**data))
                    # Create the json with the important data
                    if len(data_list) % (chunksize) == 0:
                        print("Readding chunk number:", chunk_number,
                              "in ", (time.time() - start_time)/60, "minutes")
                        logging.error("Readding chunk number: " + str(chunk_number) +
                                      "in " + str((time.time() - start_time)/60) + " minutes")
                        start_time = time.time()
                        RUC.objects.bulk_create(data_list)
                        print("Finished insterting data:",
                              (time.time() - start_time)/60, "minutes")
                        logging.error("Finished insterting data: " +
                                      str((time.time() - start_time)/60) + " minutes")
                        start_time = time.time()
                        del data_list
                        data_list = []

                    if counter % chunksize == 0:
                        chunk_number += 1

                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    logging.error(f"An error occurred: {str(e)}")

            if len(data_list):
                RUC.objects.bulk_create(data_list)
        except Exception as e:
            print('Error in add_to_database:', e)
            logging.error('Error in add_to_database: ' + str(e))

    def export_to_sqlite(self):
        try:
            print('started export_to_sqlite')
            logging.error('started export_to_sqlite')
            start_time = time.time()

            file_name = self.download_and_extract_padron()
            if file_name == 'same_padron':
                return Response({'message': 'El padron de ruc no ha cambiado...'})

            new_file_name = 'padron_reducido_ruc.zip'
            old_file_name = 'old_padron_reducido_ruc.zip'
            os.rename(new_file_name, old_file_name)

            print("Time download_and_extract_padron:",
                  (time.time() - start_time)/60, "minutes")
            logging.error("Time download_and_extract_padron: " +
                          str((time.time() - start_time)/60) + " minutes")

            start_time = time.time()
            self.extract_active_rucs(file_name)
            print("Time extract_active_rucs:",
                  (time.time() - start_time)/60, "minutes")
            logging.error("Time extract_active_rucs: " +
                          str((time.time() - start_time)/60) + " minutes")

            conn = sqlite3.connect("db.sqlite3")
            sql_cur = conn.cursor()
            print("Deleting table sunat_ruc")
            logging.error("Deleting table sunat_ruc")
            quer = sql_cur.execute("DELETE FROM sunat_ruc")
            print(f'Number of rows deleted: {quer.rowcount}')
            logging.error(f'Number of rows deleted: {quer.rowcount}')
            conn.commit()  # Don't forget to replace sql_conn with your actual connection variable
            conn.close()

            print("Start reading file")
            logging.error("Start reading file")
            with open('padron_reducido_ruc_activo.txt', 'r', encoding='ISO-8859-1') as activo_file:
                self.add_to_database(activo_file)

            with open('padron_reducido_ruc_no_activo.txt', 'r', encoding='ISO-8859-1') as activo_file:
                self.add_to_database(activo_file)

            conn = sqlite3.connect("db.sqlite3")
            sql_cur = conn.cursor()

            quer = sql_cur.execute("SELECT * FROM sunat_ruc LIMIT 10")
            rows = quer.fetchall()
            for row in rows:
                print(row)
                logging.error(row)

            return Response({'message': 'Export to SQLite completed successfully'})

        except Exception as e:
            print('Error in export_to_sqlite:', e)
            logging.error('Error in export_to_sqlite:', e)
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
