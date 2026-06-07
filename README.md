# Jill's Sandwich — API Backend

API REST para el panel de administración de un restaurante. Expone endpoints para gestionar pedidos, clientes, menú, mesas, ventas y autenticación con doble nivel de seguridad (token de acceso + token de ventas).

> **Demo en vivo:** [PENDIENTE — agregar URL de Render/Railway]  
> **Frontend:** [PENDIENTE — agregar URL de Vercel]  
> **Documentación interactiva:** `{API_URL}/docs` (Swagger UI)  
> **Video demo:** [Primera presentación en YouTube](https://youtu.be/fP-bVC3v1AU)

---

## Descripción

Este backend es la capa de servicios del sistema **Jill's Sandwich**. Persiste la información en **MySQL** mediante **SQLAlchemy** y expone una API tipada con **FastAPI** que consume el panel de administración (React).

Los módulos principales cubren:

| Módulo | Descripción |
|--------|-------------|
| **Auth** | Login JWT, verificación de ventas, cambio de contraseñas y recuperación |
| **Orders** | CRUD de pedidos, filtros, resumen del día y flujo de estados |
| **Customers** | Alta, edición y baja de clientes |
| **Menu** | Gestión de platos con precio, categoría y disponibilidad |
| **Tables** | Control de mesas y generación de QR |
| **Sales** | Resumen de ingresos y registro de pagos |

---

## Stack tecnológico

| Tecnología | Uso |
|------------|-----|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web y documentación OpenAPI |
| [SQLAlchemy 2](https://www.sqlalchemy.org/) | ORM y mapeo de entidades |
| [MySQL](https://www.mysql.com/) | Base de datos relacional |
| [PyMySQL](https://pypi.org/project/PyMySQL/) | Driver de conexión |
| [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Configuración vía `.env` |
| [python-jose](https://python-jose.readthedocs.io/) | Tokens JWT |
| [passlib + bcrypt](https://passlib.readthedocs.io/) | Hash de contraseñas |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |

---

## Herramientas de IA utilizadas

| Herramienta | Rol en el proyecto |
|-------------|-------------------|
| **Claude Code** (navegador) | Generación del código backend: modelos, servicios, routers, autenticación JWT y estructura por features |
| **Cursor** | Documentación, depuración, scripts de seed, CI/CD y preparación para despliegue |

> Detalle completo de la experiencia con IA en [`INFORME_TECNICO.md`](./INFORME_TECNICO.md).

---

## Requisitos previos

- [Python](https://www.python.org/) ≥ 3.11
- [MySQL](https://www.mysql.com/) ≥ 8.0 (local o servicio en la nube)
- Base de datos creada con las tablas del proyecto

---

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/ProyectoDeGestionDeRestaurante-Back.git
cd ProyectoDeGestionDeRestaurante-Back

# 2. Crear entorno virtual
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu DATABASE_URL y SECRET_KEY

# 5. Crear la base de datos y el primer administrador
# Solo es necesario correr este comando UNA SOLA VEZ en una instalación nueva.
# Crea la base de datos, las tablas, el menú inicial, las mesas
# y solicita interactivamente las credenciales del administrador.
python setup_db.py

# 6. Iniciar el servidor
fastapi dev main.py
```

La API estará disponible en **http://127.0.0.1:8000**.  
Documentación Swagger: **http://127.0.0.1:8000/docs**

---

## Variables de entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DATABASE_URL` | Cadena de conexión SQLAlchemy | `mysql+pymysql://root@localhost:3306/jills_sandwich` |
| `SECRET_KEY` | Clave para firmar JWT | Clave larga y aleatoria |
| `ALGORITHM` | Algoritmo JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración del token de acceso | `480` |
| `SALES_TOKEN_EXPIRE_MINUTES` | Duración del token de ventas | `15` |

---

## Credenciales de prueba

Tras ejecutar `scripts/seed_admin.py` con los valores por defecto:

| Campo | Valor |
|-------|-------|
| Usuario | `admin` |
| Contraseña | `admin1234` |
| Contraseña de ventas | `ventas1234` |

> El **token de ventas** no es una credencial fija: se obtiene en runtime vía `POST /auth/sales-verify` al ingresar la contraseña de ventas (válido 15 minutos).

---

## Modelo de datos

Entidades principales en MySQL:

| Tabla | Descripción |
|-------|-------------|
| `admin_users` | Usuarios del panel con contraseña y contraseña de ventas hasheadas |
| `customers` | Clientes identificados por teléfono |
| `tables` | Mesas con estado y token QR |
| `menu_items` | Platos del menú |
| `orders` / `order_items` | Pedidos y sus ítems |
| `payments` | Pagos asociados a pedidos |

Diagrama ERD compartido con el frontend: ver `docs/erd.png` en el repositorio unificado del TP.

---

## Autenticación

El sistema usa **dos tokens JWT**:

1. **`access_token`** — Se obtiene con `POST /auth/login`. Protege operaciones de lectura y administración general.
2. **`sales_token`** — Se obtiene con `POST /auth/sales-verify` (requiere `access_token` activo). Protege operaciones sensibles: crear/eliminar pedidos, clientes y pagos.

En las peticiones protegidas, enviar el header:

```
Authorization: Bearer <token>
```

---

## Endpoints principales

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/health` | — | Health check |
| POST | `/auth/login` | — | Iniciar sesión |
| POST | `/auth/sales-verify` | access | Obtener token de ventas |
| GET | `/orders` | access | Listar pedidos (filtros) |
| GET | `/orders/summary` | access | KPIs del día |
| POST | `/orders` | sales | Crear pedido |
| PATCH | `/orders/{id}/status` | access | Cambiar estado |
| GET/POST/PATCH/DELETE | `/customers` | access / sales | CRUD clientes |
| GET/POST/PUT/DELETE | `/menu-items` | access | CRUD menú |
| GET/POST/PUT/DELETE | `/tables` | access | CRUD mesas |
| GET | `/tables/{id}/qr` | access | QR de mesa |
| GET | `/sales/summary` | sales | Resumen de ventas |
| GET/POST/PATCH | `/sales/payments` | sales | Gestión de pagos |

Documentación completa e interactiva en `/docs`.

---

## Estructura del proyecto

```
ProyectoDeGestionDeRestaurante-Back/
├── core/               # Config, DB, seguridad, dependencias
├── features/
│   ├── auth/           # Autenticación JWT
│   ├── customers/      # Clientes
│   ├── menu/           # Menú
│   ├── orders/         # Pedidos
│   ├── sales/          # Ventas y pagos
│   └── tables/         # Mesas y QR
├── scripts/
│   └── seed_admin.py   # Crear primer administrador
├── shared/
│   └── uow.py          # Unit of Work (transacciones)
├── main.py             # Punto de entrada FastAPI
├── requirements.txt
└── .env.example
```

Arquitectura por **features**: cada módulo contiene `models.py`, `schemas.py`, `service.py` y `router.py`.

---

## Despliegue

### Render / Railway (recomendado)

1. Crear servicio web con Python 3.11
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Configurar variables de entorno (`DATABASE_URL`, `SECRET_KEY`, etc.)
5. Usar MySQL en la nube (PlanetScale, Railway MySQL, Aiven, etc.)
6. Actualizar `allow_origins` en `main.py` con la URL del frontend en Vercel

### CI/CD — GitHub Actions

El pipeline en `.github/workflows/ci.yml` verifica en cada push/PR:

- Instalación de dependencias
- Importación correcta de la aplicación

---

## Repositorios relacionados

| Repo | Descripción |
|------|-------------|
| **Frontend** | [ProyectoDeGestionDeRestaurante-Front](https://github.com/EmiG4rcia/ProyectoDeGestionDeRestaurante-Front) |
| **Backend** | Este repositorio — [PENDIENTE — URL GitHub] |

---

## Autores

Proyecto desarrollado como **Trabajo Práctico Integrador** — Tecnicatura en Programación, 4° Semestre, Gestión de Desarrollo de Software.

---

## Licencia

Este proyecto es de código abierto con fines académicos.
