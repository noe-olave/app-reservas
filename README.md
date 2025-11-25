🚀 Overview

Scheduler-API es un API RESTful dedicada a la gestión de recursos temporales y citas. Fue diseñado como un micro-servicio independiente para manejar la complejidad de la lógica de negocio de reservas, asegurando la integridad de la base de datos contra conflictos de horarios.

🛠️ Technical Stack


    Backend Framework: Python, Django REST Framework (DRF)

    Database: PostgreSQL

    Testing: Pytest (con pytest-django)

    Containerization: Docker


🏗️ Architecture & Key Features


    Validación Robusta (Integridad de Datos): La lógica de negocio fundamental del modelo (models.py) incluye validaciones en el método clean() que previenen la creación de citas que se superpongan con turnos existentes.

    Endpoints RESTful: Implementación de ViewSets completos para CRUD (Crear, Leer, Actualizar, Borrar) de citas, siguiendo patrones de diseño RESTful limpios.

    Seguridad por Diseño: Uso de permisos de DRF (IsAuthenticated) para asegurar que solo usuarios autenticados puedan reservar y que solo puedan acceder a sus propias citas.

    Calidad del Código: Inclusión de un conjunto completo de pruebas unitarias (Pytest) que verifican la lógica de validación de superposición, asegurando que las reglas de negocio sean infalibles.


🧪 Run Tests

# Se requiere tener Pytest y django instalados
pytest
