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

## 📋 Requisitos Previos

- Python 3.8 o superior
- Una API Key de Google Gemini

## 🔧 Instalación

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

## 📁 Estructura del Proyecto

```
.
├── main.py                # Script principal
├── test_pdf_extraction.py # Herramienta de prueba para extracción de PDF
├── test_process.py       # Herramienta de prueba para procesamiento
├── requirements.txt      # Dependencias del proyecto
├── .env                 # Configuración de API Key (no incluido en git)
└── README.md            # Este archivo
```

## 🚀 Uso

1. Ejecuta el script:
```bash
python main.py
```

2. Selecciona la carpeta que contiene tus archivos PDF usando el diálogo que aparece

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

- Asegúrate de mantener tu API Key segura y no compartirla
- El script procesará todos los PDFs en la carpeta seleccionada
- Los archivos de salida se crearán en una subcarpeta `output` dentro de la carpeta seleccionada
- Los archivos de salida se sobrescribirán si ya existen
- El campo `Archivo_Origen` permite rastrear de qué PDF proviene cada registro

## 📄 Licencia

[MIT License](LICENSE)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.