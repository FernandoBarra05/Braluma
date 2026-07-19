# Braluma — Sitio Web & Panel Administrativo (Fase 1)

**Braluma** es una marca especializada en la fabricación y comercialización de espejos de diseño arquitectónico con iluminación LED integrada, control de temperatura de luz Kelvin y tecnología antivaho.

Este repositorio contiene la implementación completa de la **Fase 1** del proyecto.

---

## 🌟 Características Principales de la Fase 1

1. **Hero Parallax Multicapa & Efecto Encendido LED**:
   - Hero de pantalla completa con animación de parpadeo inicial ("ignition flicker") que simula el encendido de un espejo LED.
   - Respuesta 3D con inclinación sutil al movimiento del cursor en escritorio.
   - Escala, rotación y oscurecimiento progresivo de viñeta en scroll.
   - Partículas de luz ambientales.
   - **Accesibilidad Total**: Compatible con `prefers-reduced-motion: reduce` (desactiva animaciones y renders 3D para una experiencia accesible y estática).

2. **Catálogo Público de Espejos**:
   - Ruta `/`: Catálogo rápido y limpio, filtrable dinámicamente por geometría (`Redondo`, `Ovalado`, `Rectangular`, `Arco`).
   - Visualización exclusiva del **Dial Kelvin** por producto (rango 2700K - 6500K) con indicador graduado.
   - Ficha técnica detallada (`/espejo/<slug>/`) inspirada en etiquetas industriales de productos de iluminación.

3. **Captura de Leads & Integración WhatsApp**:
   - Formulario de cotización que guarda el registro `Lead` en la base de datos antes de redirigir a WhatsApp.
   - Redirección automática a `https://wa.me/<numero>?text=<mensaje_precargado>` con datos del cliente y el modelo de espejo consultado.
   - Número de WhatsApp configurable mediante variable de entorno `WHATSAPP_NUMBER`.

4. **Panel Administrativo Personalizado (Django Admin)**:
   - Ruta `/admin/`.
   - Edición directa de `precio`, `stock`, `activo` y `destacado` desde la lista de espejos (`list_editable`) para agilizar la gestión diaria del equipo Braluma.
   - Gestión de múltiples imágenes por producto mediante `Inline` con vista previa miniatura HTML.
   - Administración de `Leads` con filtros por estado/canal, buscador y acción masiva para marcar como *"Contactado"*.

5. **Dashboard Interno de Métricas (Solo Staff)**:
   - Ruta `/panel/metricas/` protegida por autenticación y permisos `@staff_member_required`.
   - Tarjetas KPI (Total Leads, Leads Nuevos, Productos Activos).
   - Gráficos interactivos en **Chart.js** (Línea de tendencia de leads por semana de las últimas 8 semanas y Barras de espejos más consultados).

---

## 🛠️ Stack Técnico

- **Backend**: Python 3.12+ & Django (última versión estable).
- **Base de Datos**: SQLite para desarrollo local (preparado mediante abstraídas variables de entorno para migración transparente a PostgreSQL).
- **Frontend**: HTML5 + CSS3 Vanilla + JavaScript Vanilla rendered directo mediante Django Templates.
- **Procesamiento de Imágenes**: Pillow (para `ImageField`).
- **Gráficos**: Chart.js vía CDN.

---

## 🚀 Guía de Instalación y Ejecución Local

### 1. Clonar el repositorio y navegar a la carpeta
```bash
git clone <repository_url>
cd Braluma
```

### 2. Crear y activar un entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno (`.env`)
Crea un archivo `.env` en la raíz del proyecto (junto a `manage.py`) basándote en el siguiente ejemplo:

```env
SECRET_KEY=tu_clave_secreta_django_aqui
DEBUG=True
ALLOWED_HOSTS=*
WHATSAPP_NUMBER=51924280775

# Configuración de Base de Datos (Opcional - SQLite por defecto)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=braluma_db
# DB_USER=postgres
# DB_PASSWORD=tu_password
# DB_HOST=localhost
# DB_PORT=5432
```

### 5. Aplicar migraciones y ejecutar la Semilla de Datos
```bash
python manage.py migrate
python manage.py seed_data
```
> **Nota**: El comando `seed_data` creará automáticamente:
> - Superusuario de prueba: **Usuario:** `admin` / **Contraseña:** `admin123`.
> - Categorías iniciales y 6 modelos de espejos con imágenes generadas vía Pillow.
> - Datos históricos de leads de prueba para visualizar los gráficos del dashboard inmediatamente.

### 6. Iniciar el servidor local
```bash
python manage.py runserver
```

Accede al sitio en tu navegador:
- **Catálogo Público**: `http://127.0.0.1:8000/`
- **Panel Administrativo**: `http://127.0.0.1:8000/admin/`
- **Dashboard de Métricas**: `http://127.0.0.1:8000/panel/metricas/` *(Inicia sesión primero con `admin` / `admin123`)*

---

## 📊 Nota sobre Analítica de Tráfico Web

El dashboard interno en `/panel/metricas/` rastrea **métricas operativas del negocio** (leads capturados, productos más cotizados). **No reemplaza** una herramienta de analítica de tráfico general.

Para medir tráfico web, visitantes únicos, tasa de rebote y embudos de navegación en producción, se recomienda integrar:
- **Google Analytics 4 (GA4)**: Añadiendo la etiqueta `G-XXXXXXXXXX` en `templates/base.html`.
- **Umami Analytics**: Opción ligera, enfocada en la privacidad de los usuarios y libre de cookies.

---

## 🔮 Roadmap de Fases Futuras (Fuera del Alcance de la Fase 1)

Las siguientes funcionalidades están contempladas para etapas futuras de Braluma:
- [ ] Carrito de compras persistente e itinerario de selección.
- [ ] Pasarela de pagos integrada (Culqi, Niubiz, MercadoPago).
- [ ] Módulo Multi-vendedor / Marketplace.
- [ ] Facturación electrónica automatizada (SUNAT / Proveedor PSE).
