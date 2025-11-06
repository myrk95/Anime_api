# API para sugerencias de anime
Api con interfaz para cliente en web y admin en consola
---
## Funcionalidades: cliente
- Permite registro y login
- Obtiene recomendaciones de anime según las preferencias del usuario
- Permite buscar anime entre la lista de totdos los anime disponibles para recomendar

## Funcionalidades: admin
- Entrenar el algoritmo
- Cargar el modelo preexistente
- Ver todos los usuarios

## ⚙️ Iniciar Back-end

1. Instalar las librerías necesarias y generar modelos:
   ```bash
   # Permiso para ejecutar
    chmod +x backend/setup.sh
   # Ejecutar des del root del proyecto
    ./backend/setup.sh
   ```
2. Abrir un terminal dentro de la carpeta **`backend/app`** y ejecutar:
   ```bash
   python main.py
   ```
3. El servidor se ejecutará por defecto en:
   ```bash
   http://127.0.0.1:5000
   ```

## 💻 Iniciar Front-end: Cliente

1. Abrir un terminal dentro de la carpeta **`frontend/web_anime`**

## 🎮 Interactuar con la Web para cliente 

1. Login o registro
2. Una vez haya hecho registro el usuario podrá ver sus datos
4. Haz clic en el botón “Coger recomendaciones”.
5. En pocos instantes, aparecerá un modal con tus recomendaciones personalizadas.
6. Si deseas obtener recomendaciones distintas:
   - Cierra el modal haciendo clic fuera de él.
   - Repite el proceso desde el paso 2.

## 💾 Iniciar Front-end: Admin

1. Abrir un terminal dentro de la carpeta **`frontend/web_anime`** y ejecutar:
   ```bash
   python api_admin.py
   ```
## Interactuar con la API de consola para admin
Verificar que es admin mediante login
### Opciones de administrador
**1. Ver estado de la matriz:** muestra el estado actual de la matriz de correlación utilizada por el sistema de recomendaciones.

**2. Entrenar nuevo modelo:** permite reentrenar el sistema de recomendaciones con datos actualizados.

**3. Ver información de la matriz:** muestra detalles estadísticos y metadatos de la matriz de correlación.

**4. Probar recomendaciones:** permite probar el sistema de recomendaciones con un conjunto de datos de prueba o un usuario específico.

**5. Ver usuarios registrados:** lista todos los usuarios registrados en el sistema y su información básica.

**6. Salir:** cierra el panel de administración.
