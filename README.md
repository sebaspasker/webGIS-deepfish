# WebGIS Deepfish

En este repositorio vamos a encontrar todo el mecanismo del webgis de deepfish. Que a partir de información AIS y recopilación de información de Deepfish2 representará la información de manera visual en un mapa.

## Instalación 

Para la instalación se recomienda crear un entorno virtual en python y luego instalar las dependencias necesarias. 

```bash
python3 -m venv venv
pip install -r requirements.txt
```

Una vez instalado las dependencias, se puede correr el servidor con el siguiente comando de django:

```bash
python manage.py runserver
```

Hay que tener en cuenta que los datos no están subidos por temas de confidencialidad por lo que sin ellos no se podrá visualizar la información de la misma manera.
