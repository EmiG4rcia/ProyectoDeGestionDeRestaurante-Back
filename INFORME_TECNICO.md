# Informe Técnico — Backend (Bitácora de Desarrollo con IA)

**Proyecto:** Jill's Sandwich — API Backend  
**Asignatura:** Gestión de Desarrollo de Software — TP Integrador  
**Fecha:** Junio 2026

---

## 1. Resumen del backend

Desarrollamos la capa de servicios del sistema **Jill's Sandwich**: una API REST en **FastAPI** que persiste datos en **MySQL** mediante **SQLAlchemy** y expone endpoints para autenticación, pedidos, clientes, menú, mesas y ventas.

El backend fue diseñado para consumirse desde un panel de administración (React) y soporta un modelo de seguridad con **dos tokens JWT**: uno de acceso general y otro específico para operaciones de ventas.

### Alcance de este informe

Nos centramos en el **backend y la base de datos**. No profundizamos en el proyecto base del cual se desprende el TP (automatización con n8n, WhatsApp, etc.), salvo donde impacta directamente en las entidades del dominio (por ejemplo, clientes identificados por teléfono o mesas con token QR).

### Repositorios y demo

- **Frontend:** [ProyectoDeGestionDeRestaurante-Front](https://github.com/EmiG4rcia/ProyectoDeGestionDeRestaurante-Front)
- **Backend:** [PENDIENTE — URL GitHub]
- **API desplegada:** [PENDIENTE — URL Render/Railway]
- **Swagger:** `{API_URL}/docs`
- **Video demo:** [Primera presentación en YouTube](https://youtu.be/fP-bVC3v1AU)

---

## 2. Modelo de datos

### Entidades principales

| Tabla | Rol |
|-------|-----|
| `admin_users` | Administradores del panel (login + contraseña de ventas) |
| `customers` | Clientes del restaurante |
| `tables` | Mesas con estado (`available` / `occupied`) y `qr_token` |
| `menu_items` | Platos con precio, categoría y disponibilidad |
| `orders` | Pedidos con flujo de estados |
| `order_items` | Ítems de cada pedido |
| `payments` | Pagos vinculados a pedidos |

### Relaciones clave

- Un **cliente** puede tener muchos **pedidos**.
- Una **mesa** puede tener muchos **pedidos**.
- Un **pedido** contiene muchos **order_items**, cada uno referenciando un **menu_item**.
- Un **pago** pertenece a un **pedido**.

### Diagrama ERD

![Diagrama ERD del sistema](./docs/erd.png)

> **Nota:** Guardar la captura del ERD en `docs/erd.png` antes de subir el repo (puede compartirse con el frontend).

---

## 3. Arquitectura del backend

### Organización por features

Adoptamos una estructura modular donde cada dominio tiene su propio paquete:

```
features/
├── auth/       → JWT, login, verificación de ventas
├── customers/  → CRUD de clientes
├── menu/       → CRUD del menú
├── orders/     → Pedidos y estados
├── sales/      → Pagos y resumen de ventas
└── tables/     → Mesas y generación de QR
```

Cada feature contiene:

- `models.py` — Entidades SQLAlchemy
- `schemas.py` — Validación Pydantic (request/response)
- `service.py` — Lógica de negocio
- `router.py` — Endpoints FastAPI

La capa `core/` centraliza configuración (`.env`), conexión a base de datos, seguridad JWT y dependencias de autenticación.

### Autenticación dual

| Token | Tipo JWT | Duración | Uso |
|-------|----------|----------|-----|
| `access_token` | `type: access` | 480 min | Lectura, menú, mesas, cambio de estados |
| `sales_token` | `type: sales` | 15 min | Crear/eliminar pedidos, clientes y pagos |

Esta separación nos permitió implementar una **doble verificación** para operaciones sensibles sin complicar el login diario del administrador.

---

## 4. Nuestro arsenal de herramientas de IA

| Herramienta | Versión / Plan | Uso principal en el backend |
|-------------|----------------|----------------------------|
| **Claude Code** (navegador) | Pro | Generación del código backend: modelos SQLAlchemy, routers, servicios, autenticación JWT y estructura por features |
| **Cursor** | Agent mode | Documentación, depuración rápida, modificación de código, CI/CD, script de seed y preparación para despliegue |

---

## 5. Sinergia con la IA — Cómo nos ayudó a programar el backend

### 5.1 Generación de código (Claude Code)

Para generar el código del backend utilizamos **Claude Code en su versión de navegador**, mientras que reservamos **Cursor** para documentación, depuración y corrección rápida de problemas en el proyecto.

El desarrollo del backend fue impulsado principalmente por Claude, aprovechando el **contexto previo del dominio del restaurante** que ya estaba cargado en la conversación. Por eso, el prompt inicial fue **intencionalmente simple**:

**Prompt inicial (reconstruido):**

```
Necesitamos la API REST en FastAPI para el panel de administración del restaurante.
Debe cubrir autenticación, pedidos, clientes, menú, mesas y ventas,
usando SQLAlchemy con MySQL y JWT para proteger los endpoints.
```

**Tareas donde la IA fue más útil en el backend:**

- [x] Estructura por features (`auth`, `orders`, `customers`, etc.)
- [x] Modelos SQLAlchemy alineados con el ERD
- [x] Schemas Pydantic para validación de entrada/salida
- [x] Servicios con lógica de negocio (filtros, estados, totales)
- [x] Routers REST con inyección de dependencias
- [x] Autenticación JWT con dos niveles (`access` + `sales`)
- [x] Hash de contraseñas con bcrypt/passlib
- [x] Generación de QR para mesas

Los prompts que **mejor funcionaron** con Claude fueron los orientados a la **generación de la estructura del proyecto**: Claude demostró ser muy eficiente a la hora de diagramar clases, archivos y cómo estos deberían estar conectados entre sí.

### 5.2 Depuración y ajustes

El backend **funcionó desde el principio sin errores**. No tuvimos que corregir bugs en el código generado por Claude; el flujo consistió en probar la API y, cuando fue necesario, pedir ajustes puntuales.

Para depuración y correcciones rápidas durante el desarrollo y la entrega del TP, utilizamos **Cursor** por su integración con el IDE, acceso al terminal y capacidad de leer el proyecto completo.

**Estimación de tiempo:**

| Enfoque | Tiempo estimado |
|---------|-----------------|
| Con Claude Code | Menos de 2 horas |
| Manual (sin IA) | Al menos 5 horas |

### 5.3 Documentación y entrega (Cursor)

Cursor intervino en la fase de **empaquetado del TP** para el backend:

- [x] README completo del backend
- [x] Informe técnico (este documento)
- [x] `requirements.txt` con dependencias pinneadas
- [x] `.env.example` y `.gitignore`
- [x] Script `scripts/seed_admin.py` para crear el primer administrador
- [x] Pipeline CI en GitHub Actions (verificación de imports)
- [x] Planificación de las etapas de armado y entrega según consignas del TP
- [ ] Despliegue en Render/Railway — pendiente
- [ ] Documentación unificada front + back — en progreso

---

## 6. Lecciones aprendidas y desafíos

### 6.1 Lo que funcionó bien

- **Contexto previo en la conversación:** Tener el dominio del restaurante y el ERD ya cargados en Claude Code nos permitió un prompt inicial minimalista pero efectivo.
- **Eficiencia en estructura de proyecto:** Claude destacó en diagramar la arquitectura por features, las relaciones entre módulos y la organización de archivos.
- **Código funcional a la primera:** El backend corrió sin errores desde la primera iteración, lo que nos ahorró tiempo de depuración.
- **Arquitectura por features:** La separación en módulos independientes facilitó entender, extender y documentar cada dominio.
- **Consistencia con el frontend:** Al compartir contratos de API y entidades, redujimos fricción en la integración con el panel React.
- **Velocidad:** Generamos el backend en **menos de 2 horas** con IA, frente a una estimación de **al menos 5 horas** de forma manual.

### 6.2 Donde la IA requirió intervención manual

- **Credenciales iniciales:** La función `create_first_admin` existía en el código pero no estaba expuesta por API ni documentada; resolvimos esto con un script de seed creado con Cursor.
- **Preparación para producción:** Faltaban `requirements.txt`, `.gitignore`, CI/CD y guía de despliegue — tareas resueltas con Cursor.
- **Base de datos:** La conexión MySQL, creación de tablas y variables de entorno requieren configuración manual fuera del alcance del chat.
- **CORS en despliegue:** Hay que actualizar `allow_origins` en `main.py` con la URL real del frontend.

### 6.3 Desafíos técnicos específicos del backend

- **Autenticación dual:** Diseñar dos tokens JWT con distintos scopes y tiempos de expiración.
- **Operaciones con distinto nivel de acceso:** Algunos endpoints usan `get_current_admin` y otros `get_sales_access` dentro del mismo router.
- **Integridad referencial:** Pedidos vinculados a clientes, mesas e ítems del menú con totales calculados en servicio.
- **Despliegue con MySQL externo:** Configurar `DATABASE_URL` en la nube y mantener la base sincronizada con los modelos.

### 6.4 Reflexión sobre la eficiencia de la IA

Para un backend de esta escala (CRUD + auth + lógica de negocio moderada), Claude Code demostró ser **altamente eficiente** cuando:

1. El ERD y los flujos de negocio estaban claros antes de generar código
2. Confiamos en la IA para completar detalles no explicitados (schemas, enums, filtros)
3. Reservamos Cursor para depuración, documentación y empaquetado profesional

La clave fue **no sobre-explicar el prompt** cuando el contexto ya estaba cargado, y confiar en la capacidad de Claude para diagramar la estructura del proyecto de forma coherente.

---

## 7. Flujo de trabajo adoptado (backend)

```mermaid
graph LR
    A[ERD + contexto previo] --> B[Prompt simple a Claude Code]
    B --> C[API FastAPI + SQLAlchemy]
    C --> D[MySQL local]
    D --> E[Integración con frontend]
    E --> F{¿Ajustes?}
    F -->|Sí| G[Claude o Cursor según tarea]
    G --> D
    F -->|No| H[Cursor: docs + CI/CD + seed]
    H --> I[Deploy Render/Railway]
```

---

## 8. Experiencia con Cursor (documentación y organización)

### 8.1 Tareas realizadas con Cursor en el backend

- [x] README del backend
- [x] Informe técnico backend
- [x] `requirements.txt`, `.env.example`, `.gitignore`
- [x] Script de seed para administrador
- [x] GitHub Actions (CI)
- [x] Planificación de etapas de entrega del TP
- [ ] Despliegue y CORS para producción

### 8.2 ¿Qué tan útil fue Cursor vs Claude para el backend?

Cursor resultó **extremadamente útil** para generar y modificar documentación. Gracias a su capacidad de analizar y leer el proyecto al ser un agente integrado en el IDE, se convirtió en la mejor opción para documentar, modificar código de forma rápida y depurar mediante acceso al terminal para ejecutar comandos.

No identificamos una herramienta como estrictamente "mejor" que la otra; definimos con claridad en qué contextos preferimos usar cada una:

| Herramienta | Contexto preferido | Por qué |
|-------------|-------------------|---------|
| **Claude Code** (navegador) | Generar código desde cero | Es nuestro puntapié inicial. Destaca en diagramar estructura, clases y conexiones entre archivos. |
| **Cursor** (agente en IDE) | Documentación, depuración y tareas mecánicas | Integrado en el editor: lee archivos, ejecuta terminal y modifica código sin salir del entorno. |

**Ventajas concretas de Cursor que destacamos:**

- **Documentación con contexto completo:** Lee todo el proyecto y genera README e informes técnicos alineados con el código real.
- **Modificaciones iterativas sin fricción:** Cada vez que necesitamos ajustar la documentación, Cursor lo hizo sin repetir instrucciones ni sobre-explicar.
- **Depuración rápida:** Acceso directo al terminal para ejecutar comandos, verificar imports y probar scripts.
- **Comprensión de código ajeno:** Cursor también resulta muy útil para entender proyectos con código que no es propio.

En resumen: **Claude Code construye, Cursor mantiene, documenta y empaqueta.**

### 8.3 Prompts que funcionaron mejor en Cursor

Los prompts orientados a **crear documentación** y a **ir modificándola según lo que necesitábamos** en cada iteración fueron los más productivos. Pedirle a Cursor que explore el proyecto, arme README e informe técnico, y luego refinar el contenido con correcciones puntuales resultó mucho más eficiente que redactar toda la documentación manualmente.

---

## 9. Checklist de entrega (backend)

| # | Requisito | Estado |
|---|-----------|--------|
| 1 | Repo público en GitHub | ⬜ Pendiente |
| 2 | Pipeline CI/CD (GitHub Actions) | ✅ Configurado |
| 3 | Informe de herramientas de IA | ✅ Redactado |
| 4 | API desplegada y accesible | ⬜ Pendiente deploy |
| 5 | README de calidad | ✅ Creado |
| 6 | Swagger funcional en `/docs` | ✅ Incluido en FastAPI |
| 7 | Script de seed de admin | ✅ Creado |
| 8 | Documentación unificada front + back | ⬜ En progreso |

---

## 10. Conclusión

El backend de **Jill's Sandwich** demuestra cómo la IA puede acelerar la construcción de una API REST completa — con autenticación, persistencia relacional y lógica de negocio — sin sacrificar una arquitectura clara por features.

Generamos el backend en **menos de 2 horas** con Claude Code (frente a **al menos 5 horas** manualmente), y el código funcionó **desde la primera iteración sin errores**. La clave fue tener el contexto del dominio y el ERD cargados antes de pedir código, y confiar en la capacidad de Claude para diagramar la estructura del proyecto.

Cursor complementó el proceso en la fase de **empaquetado profesional**: documentación, dependencias, CI, scripts operativos y planificación de la entrega del TP — tareas que la generación inicial no cubrió por defecto.

La IA no reemplaza el criterio del equipo, pero nos permitió enfocarnos en decisiones de arquitectura (como la autenticación dual) mientras delegábamos la implementación repetitiva de CRUDs, schemas y routers.
