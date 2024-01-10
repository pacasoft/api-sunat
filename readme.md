# API SUNAT

Descripción corta del proyecto.

## Indice

- [Instalación](#instalación)

  - [Dependencias](#dependencias)
  - [Ambiente virtual](#ambiente-virtual)
  - [Instalar paquetes](#instalar-django-y-otros-paquetes-utilizados)

- [Uso](#uso)
- [Endpoints](#endpoints)
- [Pruebas](#pruebas)
- [Changelog](#changelog)

# Instalación

### Dependencias

- [Python 3.9](https://www.python.org/downloads)
- [Django 4.2.9](https://www.djangoproject.com/download/)

### Ambiente virtual

Para desarrollar y ejecutar tu proyecto, se recomienda utilizar un ambiente virtual:

1.  **Abrir una Terminal:**

    Abre una terminal en el directorio de tu proyecto.

2.  **Crear un Ambiente Virtual:**

    Ejecuta el siguiente comando para crear un nuevo ambiente virtual llamado "env":

         python -m venv env

3.  **Activar ambiente virtual**

    - En sistemas basados en Unix/Linux/macOS:

            source env/bin/activate

    - En windows:

            .\env\Scripts\activate

### Instalar Django y otros paquetes utilizados

Todos los paquetes utilizados se encuentran en el archivo requirements.txt.

Asegúrate de tener Python y pip instalados para instalar rapidamente las dependencias dentro de requirements.txt.

    pip install -r requirements.txt

# Uso

1.  **Inicia el ambiente virtual**

        source env/Scripts/activate

2.  **Navega a la carpeta principal**

        cd ./src

3.  **Ejecuta el servidor de desarrollo**

        python manage.py runserver

    La API estará disponible en http://localhost:8000/.

4.  **De no tener la base de datos creada, ejecute los comandos:**

        python manage.py makemigrations
        python manage.py migrate

# Endpoints

- GET /api/v1/dni/:numero: Obtiene los datos de una persona a traves del número de DNI
- GET /api/v1/ruc/:numero: Obtiene los datos de una empresa a traves del número de RUC

# Pruebas

Aún no existe ninguna prueba implementada

# Changelog

## v1.0.0 - 20-01-2024

- Busqueda de datos personales a traves del número de DNI o RUC
- Actualización automática del padrón de RUCs

## v0.1 - 10-01-2024

- Creación de REST API en Django (T-314)
- Creación de base de datos (T-312)
- Configuración de endpoints (T-315)
