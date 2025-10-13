# Extractor de Datos de PDF con Gemini AI

Este proyecto es una herramienta que extrae datos estructurados de archivos PDF utilizando la API de Google Gemini AI. Está diseñado específicamente para procesar documentos financieros y convertirlos en formato CSV.

## 🌟 Características

- Extracción de texto de archivos PDF
- Procesamiento de texto utilizando Google Gemini AI
- Conversión automática a formato CSV
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
├── main.py              # Script principal
├── my_pdfs/            # Directorio para PDFs de entrada
├── output/             # Directorio para CSVs generados
├── requirements.txt    # Dependencias del proyecto
├── .env               # Configuración de API Key (no incluido en git)
└── README.md          # Este archivo
```

## 🚀 Uso

1. Coloca tus archivos PDF en la carpeta `my_pdfs/`

2. Ejecuta el script:
```bash
python main.py
```

3. Los archivos CSV generados se guardarán en la carpeta `output/`

## 📊 Formato de Salida

El script genera archivos CSV con los siguientes campos:
- referencia_unica
- nombre_librado
- iban
- importe
- vencimiento
- emisor
- identificacion_emisor
- referencia_fichero
- fecha_recepcion
- fecha_documento
- referencia_documento

## ⚠️ Notas Importantes

- Asegúrate de mantener tu API Key segura y no compartirla
- El script procesa todos los PDFs en la carpeta `my_pdfs/`
- Los archivos de salida se sobrescribirán si tienen el mismo nombre

## 📄 Licencia

[MIT License](LICENSE)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.