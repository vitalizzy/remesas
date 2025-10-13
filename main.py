import os
import fitz  # PyMuPDF
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from io import StringIO
import re

def extraer_texto_pdf(ruta_pdf: str) -> str:
    """
    Extrae el texto de un archivo PDF manteniendo un orden de lectura lógico,
    similar a como lo haría un usuario.
    """
    try:
        documento = fitz.open(ruta_pdf)
        texto_completo = ""
        for pagina in documento:
            # Usar sort=True para un orden de lectura más natural, crucial para tablas
            texto_completo += pagina.get_text(sort=True) + "\n"
        documento.close()
        return texto_completo.strip()
    except Exception as e:
        print(f"❌ Error al leer el PDF {ruta_pdf}: {e}")
        return ""

def estructurar_informacion_con_gemini(texto_pdf: str) -> str:
    """
    Envía el texto extraído a Gemini y le pide que estructure los datos
    en formato TSV (Tab-Separated Values).
    """
    # Usamos el modelo 'flash' que es rápido y eficiente, como solicitaste.
    # Nota: 'gemini-2.5-flash' no es un modelo válido actualmente. Usamos 'gemini-1.5-flash-latest'.
    model = genai.GenerativeModel('models/gemini-2.5-flash')

    # Prompt ajustado a tus especificaciones, con instrucciones claras para el formato de salida.
    prompt = f"""
Te voy a dar el texto de un pdf pegado aqui y tu tienes que estructurar los datos de la siguiente manera:

El formato de salida debe ser un fichero TSV (valores separados por tabuladores) SIN LÍNEA DE CABECERA.

El orden EXACTO de las columnas debe ser:
Referencia Única\tNombre del Librado\tIBAN\tImporte\tVencimiento\tEmisor\tIdentificación del Emisor\tReferencia del Fichero\tFecha de Recepción\tFecha del Documento\tReferencia Única del Documento

INSTRUCCIONES IMPORTANTES:
1.  Hay campos que son de encabezado (Emisor, Identificación del Emisor, Referencia del Fichero, Fecha de Recepción, Fecha del Documento). Estos campos se repiten en CADA LÍNEA del TSV que generes. Rellena el mismo valor para todas las filas.
2.  Los otros campos (Referencia Única, Nombre del Librado, IBAN, Importe, Vencimiento, Referencia Única del Documento) son específicos de cada línea de detalle del documento.
3.  Si un campo no se encuentra, utiliza la palabra 'null'.
4.  El importe debe ser un número decimal usando el punto (.) como separador, sin símbolo de moneda ni separadores de miles.
5.  Las fechas deben estar en formato DD/MM/YYYY.
6.  NO incluyas la línea de cabecera en tu respuesta. Devuelve únicamente los datos.
7.  Asegúrate de que cada línea de tu respuesta corresponda a una línea de detalle del documento.
8.  La columna Importe debe ser un número decimal (float).

Texto del documento a procesar:
---
{texto_pdf}
---
"""

    try:
        respuesta = model.generate_content(prompt)
        
        # Limpieza básica para eliminar bloques de código de Markdown si el modelo los añade
        texto_limpio = re.sub(r'```[a-zA-Z]*\n', '', respuesta.text)
        texto_limpio = texto_limpio.replace('```', '').strip()
        
        if not texto_limpio:
            print("❌ Error: Respuesta vacía del modelo de Gemini.")
            return None
            
        return texto_limpio
        
    except Exception as e:
        print(f"❌ Error al procesar con Gemini: {e}")
        return None

def procesar_pdf(ruta_pdf: str) -> bool:
    """
    Procesa un archivo PDF: extrae texto, lo estructura con Gemini y genera un archivo TSV.
    Retorna True si el proceso fue exitoso, False en caso contrario.
    """
    print(f"\n=== Procesando: {os.path.basename(ruta_pdf)} ===")
    
    # 1. Extraer texto del PDF (simulando Ctrl+A)
    texto = extraer_texto_pdf(ruta_pdf)
    if not texto:
        return False
    print(f"✅ Texto extraído ({len(texto)} caracteres).")
    
    # 2. Procesar con Gemini para obtener el TSV
    datos_tsv = estructurar_informacion_con_gemini(texto)
    if not datos_tsv:
        return False
    print("✅ Datos estructurados por Gemini.")
    
    # 3. Crear DataFrame y guardar el archivo TSV
    try:
        columnas = [
            'Referencia Única', 'Nombre del Librado', 'IBAN', 'Importe', 
            'Vencimiento', 'Emisor', 'Identificación del Emisor', 
            'Referencia del Fichero', 'Fecha de Recepción', 'Fecha del Documento', 
            'Referencia Única del Documento'
        ]
        
        # Usamos StringIO para leer la cadena de texto TSV como si fuera un archivo
        df = pd.read_csv(StringIO(datos_tsv), sep='\t', header=None, names=columnas)
        
        # Asegurarse de que el directorio de salida existe
        os.makedirs("output", exist_ok=True)
        
        nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]
        ruta_salida = os.path.join("output", f"{nombre_base}.tsv")
        
        df.to_csv(ruta_salida, sep='\t', index=False, encoding='utf-8')
        
        print(f"✅ TSV creado exitosamente en: {ruta_salida}")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear el archivo TSV: {str(e)}")
        print("--- Datos recibidos de Gemini ---")
        print(datos_tsv)
        print("---------------------------------")
        return False

def main():
    """
    Función principal que procesa todos los PDFs en el directorio `my_pdfs`.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Error: No se encontró la variable de entorno GOOGLE_API_KEY en el archivo .env")
        return
    genai.configure(api_key=api_key)
    print("✓ API Key de Google configurada.")
    
    directorio_pdfs = "my_pdfs"
    if not os.path.exists(directorio_pdfs):
        print(f"❌ Error: El directorio '{directorio_pdfs}' no existe. Por favor, créalo y añade tus PDFs.")
        return
        
    archivos_pdf = [f for f in os.listdir(directorio_pdfs) if f.lower().endswith('.pdf')]
    if not archivos_pdf:
        print(f"ℹ️ No se encontraron archivos PDF en el directorio '{directorio_pdfs}'.")
        return
        
    print(f"📁 Encontrados {len(archivos_pdf)} PDF(s) para procesar.")
    
    exitos = sum(1 for archivo in archivos_pdf if procesar_pdf(os.path.join(directorio_pdfs, archivo)))
    
    print("\n=== Resumen del Procesamiento ===")
    print(f"Total de archivos: {len(archivos_pdf)}")
    print(f"✅ Procesados exitosamente: {exitos}")
    print(f"❌ Fallidos: {len(archivos_pdf) - exitos}")

if __name__ == "__main__":
    main()