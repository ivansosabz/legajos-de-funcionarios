# 📂 Sistema de Gestión de Legajos de Funcionarios

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

Sistema integral para la gestión digitalizada de legajos de funcionarios públicos. Desarrollado con Django, permite el registro, organización y consulta eficiente de toda la información relevante del personal.

## ✨ Características principales

- 🗃️ Gestión centralizada de legajos digitales
- 🔍 Búsqueda y filtrado avanzado de funcionarios
- 📄 Digitalización de documentos asociados
- 🔐 Control de accesos y permisos por roles
- 📊 Reportes y estadísticas del personal
- 🚀 Interfaz intuitiva y responsive

## 🛠️ Stack Tecnológico

| Tecnología       | Uso                          |
|------------------|------------------------------|
| Python 3.x       | Lenguaje principal           |
| Django           | Framework backend            |
| Bootstrap 5      | Estilos y componentes UI     |
| SQLite           | Base de datos (desarrollo)   |
| PostgreSQL       | Base de datos (producción)   |
| Git + GitHub     | Control de versiones         |

## 🚀 Instalación y Configuración

### Requisitos previos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Pasos para desarrollo

1. Clonar el repositorio:
```bash
git clone https://github.com/ivansosabz/legajos-de-funcionarios.git
cd legajos-de-funcionarios
```
2. Configurar entorno virtual:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```
3. Instalar dependencias
```bash
pip install -r requirements.txt
```
4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```
5. Migraciones e iniciar el servidor:
```bash
python manage.py migrate
python manage.py runserver
```

## 🤝 Guía de Contribución
Flujo de trabajo recomendado
1. Crear una issue para discutir los cambios propuestos
2. Sincronizar tu fork (si no eres colaborador directo)
3. Crear una rama descriptiva:

```bash
git checkout -b tipo/descripcion-breve
# Ejemplos:
# feature/auth-system
# bugfix/login-validation
# docs/readme-update
```
4. Hacer commits atómicos con mensajes claros:
```bash
git commit -m "feat: añade validación de campos obligatorios"
git commit -m "fix: corrige error en cálculo de antigüedad"
```
5. Subir cambios y crear Pull Request:
```bash
git push origin tu-rama
```
## 📌 Convenciones

### 🌿 Estructura de ramas

- `feature/`: Nuevas funcionalidades  
  Ejemplo: `feature/user-authentication`

- `bugfix/`: Corrección de errores  
  Ejemplo: `bugfix/login-validation`

- `hotfix/`: Correcciones urgentes  
  Ejemplo: `hotfix/security-patch`

- `docs/`: Mejoras en documentación  
  Ejemplo: `docs/api-reference`

### ✏️ Estilo de commits

| Prefijo    | Descripción                                      | Ejemplo                          |
|------------|--------------------------------------------------|----------------------------------|
| `feat:`    | Nueva funcionalidad                              | `feat: add user profile page`    |
| `fix:`     | Corrección de bugs                               | `fix: resolve login timeout`     |
| `docs:`    | Cambios en documentación                         | `docs: update installation guide`|
| `refactor:`| Refactorización de código                       | `refactor: user model methods`   |
| `style:`   | Cambios de formato (sin afectar funcionalidad)   | `style: fix code indentation`    |
| `test:`    | Pruebas nuevas o correcciones                   | `test: add login tests`          |

**Ejemplo completo:**
```bash
git commit -m "feat: implement password reset functionality"
```
## 📄 Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).  

[![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 👥 Equipo

| Nombre            | Rol                     | Contacto                          |
|-------------------|-------------------------|-----------------------------------|
| Iván Sosa         | Desarrollador           | [@ivansosabz](https://github.com/ivansosabz) |
| Rossmary Villalba | Desarrolladora          | [@rossmaryv](https://github.com/rossmaryv)   |


