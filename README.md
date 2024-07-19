# Introduction

Este proyecto es una aplicación que integra y sincroniza datos entre Odoo y una base de datos local. La aplicación se
centra en la creación, eliminación, actualización y obtención de registros de leads y partners en Odoo, con capacidad
para detectar y corregir datos incorrectos.

La idea es poder extender la aplicación en el futuro con otras funcionalidades de Odoo y mejorar la gestión de los
datos.

# Getting Started

Para poner en marcha este proyecto en tu propio sistema, sigue los siguientes pasos:

## 1. Instalación

Clona el repositorio e instala las dependencias:

```bash
git clone <tu-repositorio>
cd <tu-repositorio>
pip install -r requirements.txt
```

## 2. Dependencias de Software

Las principales dependencias de software incluyen:

- Python 3.8+
- Levenshtein
- Odoo API client

## 3. Últimas Versiones

Asegúrate de tener las últimas versiones de las dependencias. Puedes actualizar usando `pip`:

```bash
pip install --upgrade -r requirements.txt
```

## 4. Referencias de API

Este proyecto utiliza la API de Odoo para interactuar con los datos. Asegúrate de tener acceso a la API de Odoo con las
credenciales adecuadas.

# Build and Test

Para construir y probar el código, sigue estos pasos:

## 1. Ejecución del Código

Ejecuta el script principal para iniciar la sincronización y corrección de datos:

```bash
python main.py
```

## 2. Pruebas

Asegúrate de que todos los componentes funcionan correctamente mediante pruebas unitarias. Puedes agregar tus pruebas en
la carpeta `tests` y ejecutarlas con `pytest`:

```bash
pytest 
```
# Contribute

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Agregar nueva funcionalidad'`).
4. Sube la rama (`git push origin feature/nueva-funcionalidad`).
5. Crea un Pull Request.

# Extensibilidad

Este proyecto está diseñado para ser extendido en el futuro con más funcionalidades de Odoo. Si deseas agregar nuevas
características, sigue las instrucciones en la sección Contribute.