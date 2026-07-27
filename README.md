# Proyecto FastAPI

Proyecto desarrollado con FastAPI. La organización del código queda libre para
adaptarla a las necesidades del proyecto.

## Requisitos

- Python 3.11 o superior
- Un entorno virtual de Python

## Instalación

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

El directorio incluye un `.env` para desarrollo local. También puedes volver a
crearlo a partir del archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

No guardes contraseñas o claves reales en `.env.example`. El archivo `.env`
está excluido de Git.

## Ejecutar la aplicación

```powershell
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en
<http://127.0.0.1:8000/docs>.

El registro de usuarios está disponible mediante:

```text
POST http://127.0.0.1:8000/auth/register
```

## MySQL

La conexión local utiliza las variables `MYSQL_*` del archivo `.env`.
Antes de registrar usuarios, configura `MYSQL_PASSWORD` con la contraseña
local de MySQL. Al iniciar la aplicación se crearán automáticamente la base de
datos `fastapi_db` y la tabla `users`.

Datos de la conexión para MySQL Workbench:

- Host: `127.0.0.1`
- Puerto: `3307`
- Usuario: `root`
- Esquema: `fastapi_db`
