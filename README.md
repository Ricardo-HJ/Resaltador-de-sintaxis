# Resaltador de Sintaxis

Este proyecto es un resaltador de sintaxis para tres lenguajes de programación: BASIC, Python y SQL. El objetivo es identificar y resaltar diferentes componentes del código fuente, como palabras clave, literales, operadores, separadores, comentarios e identificadores, utilizando diferentes colores.

## Cómo usar

### Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/Ricardo-HJ/Resaltador-de-sintaxis.git
    cd Resaltador-de-sintaxis
    ```

2. Asegúrate de tener Python instalado. Este proyecto usa Python 3.x.

### Ejecución

Para cada uno de los resaltadores, puedes ejecutar el script correspondiente. A continuación se muestran los pasos para ejecutar cada resaltador con sus respectivos archivos de entrada.

#### Resaltador de BASIC

1. Coloca tu archivo BASIC en el mismo directorio del script y nómbralo `input.vbs`.
2. Ejecuta el script `Resaltador_BASIC.py`:

    ```bash
    python Resaltador_BASIC.py
    ```

3. Ingresa `input.vbs` cuando se te solicite la ruta del archivo.
4. El archivo HTML resultante se guardará como `BASIC_Resaltado.html`.

#### Resaltador de Python

1. Coloca tu archivo Python en el mismo directorio del script y nómbralo `input.py`.
2. Ejecuta el script `Resaltador_python.py`:

    ```bash
    python Resaltador_python.py
    ```

3. Ingresa `input.py` cuando se te solicite la ruta del archivo.
4. El archivo HTML resultante se guardará como `Python_Resaltado.html`.

#### Resaltador de SQL

1. Coloca tu archivo SQL en el mismo directorio del script y nómbralo `input.sql`.
2. Ejecuta el script `Resaltador_SQL.py`:

    ```bash
    python Resaltador_SQL.py
    ```

3. Ingresa `input.sql` cuando se te solicite la ruta del archivo.
4. El archivo HTML resultante se guardará como `SQL_Resaltado.html`.

#### Resaltador Paralelo con Pool

1. Coloca tus archivos en el mismo directorio del script.
2. Ejecuta el script `Resaltador_paralelo_pool.py`:

    ```bash
    python Resaltador_paralelo_pool.py
    ```

3. Ingresa las rutas de los archivos cuando se te solicite.
4. Los archivos HTML resultantes se guardarán con el nombre original seguido de `[lenguaje]_resaltado.html`.

#### Resaltador Paralelo con Threading

1. Coloca tus archivos en el mismo directorio del script.
2. Ejecuta el script `Resaltador_paralelo_threading.py`:

    ```bash
    python Resaltador_paralelo_threading.py
    ```

3. Ingresa las rutas de los archivos cuando se te solicite.
4. Los archivos HTML resultantes se guardarán con el nombre original seguido de `[lenguaje]_resaltado.html`.


## Contribuidores

- María Renée Ramos Valdez A01252966
- Diego Sánchez Magaña A01722345
- Mauricio Noriega Chapa A01722543
- Ricardo Antonio Hernández Jiménez A00837337

## Estructura del Proyecto

El proyecto contiene los siguientes archivos:

- `Resaltador_BASIC.py`: Script para resaltar sintaxis BASIC.
- `Resaltador_python.py`: Script para resaltar sintaxis Python.
- `Resaltador_SQL.py`: Script para resaltar sintaxis SQL.
- `input.vbs`: Archivo de prueba para BASIC.
- `input.py`: Archivo de prueba para Python.
- `input.sql`: Archivo de prueba para SQL.

## Enlaces

- [Repositorio en GitHub](https://github.com/Ricardo-HJ/Resaltador-de-sintaxis)
