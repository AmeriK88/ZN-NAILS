# 💅 **Zemar Nails Salon** 🌟

## 📝 **Descripción**

Zemar Nails Salon es una aplicación web moderna y funcional, diseñada para gestionar reservas de citas, servicios personalizados y reportes para salones de uñas. Los usuarios pueden reservar citas fácilmente, visualizar sus citas activas y pasadas, y explorar servicios con detalles claros y visuales. La aplicación también incluye reportes diarios y mensuales, panel de administración personalizado y notificaciones automáticas. Construida con **Django** y **Bootstrap**, esta solución es escalable, segura y fácil de usar.

---

## 🛠️ **Tecnologías Utilizadas**

| **Tecnología**    | **Descripción**                                |
|--------------------|-----------------------------------------------|
| 🐍 **Django**      | Framework backend para una gestión robusta.  |
| 🎨 **Bootstrap**   | Diseño moderno, responsivo y estilizado.     |
| 🗄️ **MySQL**       | Base de datos escalable para múltiples usuarios. |
| 📊 **Matplotlib**  | Generación de gráficos para reportes.        |
| 📦 **Django Suit** | Personalización avanzada del panel de administración. |
| 🔐 **reCAPTCHA**   | Seguridad adicional contra bots.             |
| 🔔 **Notificaciones por Email** | Confirmaciones, modificaciones y recordatorios automáticos. |

---

## 📂 **Estructura del Proyecto**

El proyecto está organizado en aplicaciones específicas para una mejor escalabilidad y mantenimiento:

### 1. **Appointments**

- **Modelos**: 
  - `Appointment`: Representa citas con usuario, servicio, fecha y hora.
  - `Bloqueo de Fechas`: Representa las fechas no disponibles para reservar.
- **Vistas**: 
  - Crear, editar y cancelar citas.
  - Validación de fechas y horarios ocupados.

### 2. **Core**

- **Modelos**: 
  - `MensajeEspecial`: Representa mensajes informativos de la plataforma para informar a los usuarios.

### 3. **Services**

- **Modelos**: 
  - `Service`: Representa servicios ofrecidos con nombre, descripción, precio e imagen.
- **Vistas**: 
  - Mostrar todos los servicios disponibles.

### 4. **Reports**

- **Modelos**: 
  - `ReporteDiario`: Reporte de citas e ingresos diarios.
  - `ReporteMensual`: Reporte de citas e ingresos mensuales.
- **Funcionalidades**: 
  - Generación y descarga de reportes.
  - Visualización en el panel de administración.

### 5. **Users**

- **Modelos**: 
  - `UserProfile`: Información adicional del usuario.
- **Vistas**: 
  - Registro, inicio de sesión y perfil de usuario.

---

## 🚀 **Características Principales**

✅ **Gestión de Usuarios:**  
- Registro e inicio de sesión seguro.
- Perfil de usuario personalizable.

✅ **Reservas de Citas:**  
- Crear, modificar y cancelar citas fácilmente.
- Gestión dinámica de fechas bloqueadas y horarios ocupados.

✅ **Gestión de Servicios:**  
- Servicios presentados con detalles claros e imágenes.

✅ **Reportes Dinámicos:**  
- Generación de reportes diarios y mensuales con gráficos.
- Descarga de reportes en formato `.txt`.

✅ **Notificaciones Automáticas:**  
- Confirmaciones de citas, recordatorios y cancelaciones por correo electrónico.

✅ **Panel de Administración Personalizado:**  
- Integración con Django Suit para mejorar la experiencia del administrador.

✅ **Seguridad Mejorada:**  
- Implementación de reCAPTCHA para prevenir bots y mejorar la seguridad.

---

## ⚙️ **Instalación**

### **1. Requisitos Previos**
- Python 3.8 o superior.
- Django 3.2 o superior.

## Instala las depencias

pip install -r requirements.txt


## 🔒 Licencia

Este proyecto, Cabigote Barber Shop, desarrollado por José Félix Gordo Castaño, está licenciado para uso exclusivo con fines educativos y de aprendizaje. No se permite su venta, redistribución comercial o cualquier uso con fines de lucro sin autorización expresa del autor.