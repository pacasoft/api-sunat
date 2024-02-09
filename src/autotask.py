
from sunat.extract_padron import ExtractPadron
import os
os.environ['OPENBLAS_NUM_THREADS'] = '4'


def actualizar_padron_sunat():
    try:
        print("Is trying to check comprobantes enviados")
        extractPadron = ExtractPadron()
        extractPadron.export_to_sqlite()
    except Exception as e:
        print("Exception in actualizar_padron_sunat:", e)
