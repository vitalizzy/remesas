# Extractor de Datos de PDF con Gemini AI

Este proyecto es una herramienta que extrae datos estructurados de archivos PDF utilizando la API de Google Gemini AI. Está diseñado específicamente para procesar documentos financieros y convertirlos en formato TSV (Tab-Separated Values) con seguimiento del origen de los datos.

## 🌟 Características

- Selector de carpeta integrado para elegir la ubicación de los PDFs
- Extracción de texto de archivos PDF con ordenamiento natural
- Procesamiento de texto utilizando Google Gemini AI
- Conversión automática a formato TSV
- Combinación automática de múltiples archivos en un solo TSV
- Seguimiento del archivo de origen para cada registro
- Extracción de campos específicos como:
  - Referencia Única
  - Nombre del Librado
  - IBAN
  - Importe
  - Vencimiento
  - Emisor
  - Identificación del Emisor
  - Referencia del Fichero
  - Fechas (Recepción, Documento)
  - Archivo de Origen

## 📋 Opciones de Instalación

### Opción 1: Para Usuarios Finales (Sin necesidad de Python)

1. Descarga el archivo `Extractor_Remesas.exe` de la sección [Releases](../../releases)
2. Descarga el archivo de configuración `.env` proporcionado
3. Coloca ambos archivos en la misma carpeta
4. Edita el archivo `.env` con tu API Key de Google Gemini

### Opción 2: Para Desarrolladores (Con Python)

Requisitos:
- Python 3.8 o superior
- Una API Key de Google Gemini

Pasos:
1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd <nombre-del-directorio>
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Unix o MacOS:
source .venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura tu API Key:
- Crea un archivo `.env` en el directorio raíz
- Añade tu API Key de Google Gemini:
```
GOOGLE_API_KEY=tu_api_key_aqui
```

### Creación del Ejecutable (Para Desarrolladores)

Si deseas crear tu propio ejecutable:

1. Asegúrate de tener todas las dependencias instaladas:
```bash
pip install -r requirements.txt
```

2. Ejecuta el script de construcción:
```bash
python build_exe.py
```

3. El ejecutable se creará en la carpeta `dist` como `Extractor_Remesas.exe`

## 📁 Estructura del Proyecto

```
.
├── main.py                # Script principal
├── build_exe.py          # Script para crear el ejecutable
├── test_pdf_extraction.py # Herramienta de prueba para extracción de PDF
├── test_process.py       # Herramienta de prueba para procesamiento
├── resources/           # Recursos del proyecto (iconos, etc.)
├── requirements.txt     # Dependencias del proyecto
├── .env                # Configuración de API Key (no incluido en git)
└── README.md           # Este archivo
```

### Archivos Generados
```
.
├── build/              # Archivos temporales de construcción
├── dist/              # Contiene el ejecutable final
└── Extractor_Remesas.spec  # Especificaciones de PyInstaller
```

## 🚀 Uso

### Para usuarios con Python instalado:

1. Ejecuta el script:
```bash
python main.py
```

2. Selecciona la carpeta que contiene tus archivos PDF usando el diálogo que aparece

### Para usuarios sin Python (usando el ejecutable):

1. Descarga el archivo `Extractor_Remesas.exe` de la sección de releases
2. Haz doble clic en `Extractor_Remesas.exe`
3. Selecciona la carpeta que contiene tus archivos PDF usando el diálogo que aparece

### Para crear el ejecutable (desarrolladores):

1. Instala todas las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecuta el script de construcción:
```bash
python build_exe.py
```

3. El ejecutable se creará en la carpeta `dist` como `Extractor_Remesas.exe`

3. El script:
   - Procesará todos los PDFs en la carpeta seleccionada
   - Creará una subcarpeta `output` en la misma ubicación
   - Generará un archivo TSV individual para cada PDF
   - Creará un archivo combinado `todos_los_documentos.tsv` con todos los registros

## 📊 Formato de Salida

El script genera archivos TSV con los siguientes campos:
- Referencia Única
- Nombre del Librado
- IBAN
- Importe
- Vencimiento
- Emisor
- Identificación del Emisor
- Referencia del Fichero
- Fecha de Recepción
- Fecha del Documento
- Referencia Única del Documento
- Archivo_Origen

### 📑 Archivos Generados

El script genera dos tipos de archivos en la carpeta `output`:
1. Archivos individuales: `[nombre_del_pdf].tsv` para cada PDF procesado
2. Archivo combinado: `todos_los_documentos.tsv` con todos los registros

## ⚠️ Notas Importantes

### Seguridad y Configuración
- Asegúrate de mantener tu API Key segura y no compartirla
- El archivo `.env` debe estar en la misma carpeta que el ejecutable
- Si usas el ejecutable, es normal que algunos antivirus muestren una advertencia la primera vez

### Uso y Procesamiento
- El script procesará todos los PDFs en la carpeta seleccionada
- Los archivos de salida se crearán en una subcarpeta `output` dentro de la carpeta seleccionada
- Los archivos de salida se sobrescribirán si ya existen
- El campo `Archivo_Origen` permite rastrear de qué PDF proviene cada registro

### Requisitos del Sistema
- Sistema operativo: Windows 10/11
- Espacio en disco: ~100MB para el ejecutable
- Memoria RAM: Mínimo 4GB recomendado
- Conexión a Internet: Requerida para la API de Gemini

### Solución de Problemas
- Si el programa no inicia, verifica que el archivo `.env` esté presente y contenga la API Key
- Si recibes un error de la API, verifica tu conexión a Internet y la validez de tu API Key
- Para problemas con archivos específicos, revisa que los PDFs no estén corruptos o protegidos

## 📄 Licencia

[MIT License](LICENSE)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.