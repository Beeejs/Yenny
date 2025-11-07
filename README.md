### 📚 YENNY (Librería) - Sistema de Gestión de Libros y Ventas

**Autores:** Anthony Salazar, Facundo Marconi, Lukas Galarza y Mariano Williams 
**Curso:** Análisis y Metodología de Sistemas 
**Institución:** Da Vinci

Este documento describe el proyecto de análisis y diseño de un sistema de gestión para la librería YENNY, enfocado en optimizar la administración de inventario y ventas, desarrollado en Python con el framework Flask.

---

### 📖 Descripción General del Proyecto

El objetivo principal es desarrollar un sistema robusto y escalable que permita a los empleados de la librería YENNY realizar las siguientes tareas de manera eficiente:

* **Gestión de Librios y sus categorías:** 
* **Gestión de Ventas:**
* **Reportes:** Generación de informe de venta diarías y popularidad de los libros.

---

### ⭐ Características Destacadas

* **Arquitectura Limpia (Clean Architecture):** Implementación de capas de dominio, datos y presentación para asegurar mantenibilidad y testabilidad.
* **Tecnología Backend:** Uso de **Flask** para el desarrollo de APIs RESTful.
* **Validación Estricta:** Uso de **Pydantic** para la validación de datos en todas las capas de la aplicación.
* **Comandos CLI Personalizados:** Utilización del *command line interface* de Flask para tareas de administración, como la creación inicial de usuarios.

---

### 💻 Estructura del Proyecto

El proyecto sigue una estructura modular para separar las responsabilidades, facilitando el desarrollo y las pruebas unitarias.

***

```sh 
├── data
│   ├── adapter
│   ├── database
│   ├── repositories
│   └── utils
├── domain
│   ├── entities
│   ├── managers
│   └── validations
├── presentation
│   ├── commands
│   ├── controllers
│   ├── middlewares
│   ├── routes
├── test
```

---

## 🛠️ Instalación y Ejecución

### Requisitos

Asegúrate de tener **Python 3.x** instalado.

### 1. Preparar entorno virtual

Instalar nuestro entorno virtual.
```bash
python -m venv .venv
```

Luego de eso en la linea de comandos activarlo:

```bash
.\.venv\Scripts\activate
```

Cabe aclarar que si su sistema operativo es Windows y utiliza poweshell para permitir que se ejcuten `scripts locales` como el .venv se utiliza:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```



### 2. Instalación de Dependencias

Ejecuta el siguiente comando para instalar todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

### 3. Creación de Base de Datos

Ejecutar el siguiente comando para crear la base de datos en el apartado dee `data/database`:

```bash
py main.py
```

### 4. Creación del Usuario Administrador Inicial

Antes de iniciar el servidor, es necesario crear la cuenta de administrador inicial. Este comando utiliza un comando CLI personalizado:

```bash
flask --app presentation.app:create_app create-admin --email admin@admin
```

### 5. Ejecución del Servidor

Para iniciar la aplicación en modo de desarrollo, utiliza el siguiente comando. El flag `--debug` permite la recarga automática ante cambios:

```bash
flask run --debug
```

### 6. Ejecución del Servidor

Para verificar el correcto funcionamiento de las capas del Dominio y Repositorios, ejecuta el siguiente comando:

```bash
pytest -v
```


### 🔗 Integración y Pruebas con Postman
La colección completa de la API, incluyendo todos los endpoints necesarios para probar el sistema, está disponible públicamente en **Postman**:

**[Colección Pública de Postman (YENNY API)](https://fm-team04.postman.co/workspace~ac37aca3-35ee-4b9d-80a9-8d4d65df6713/folder/26505099-db8f7d64-45b2-4688-b56b-04e95281f226?action=share&source=copy-link&creator=26505099&ctx=documentation)**

Se recomienda importar esta colección para realizar pruebas manuales contra el servidor local de Flask.