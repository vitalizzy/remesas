import os
import json
import fitz
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog

def test_procesamiento_completo(ruta_pdf: str) -> None:
    """
    Prueba el proceso completo de extracción y estructuración de datos,
    mostrando los resultados intermedios.
    """
    print("\n=== Test de Procesamiento Completo ===")
    print(f"Archivo: {os.path.basename(ruta_pdf)}")
    print("-" * 50)

    # 1. Extracción de texto
    print("\n1️⃣ Extrayendo texto del PDF...")
    try:
        documento = fitz.open(ruta_pdf)
        texto = ""
        for pagina in documento:
            texto += pagina.get_text()
        documento.close()
        
        if not texto.strip():
            print("❌ Error: No se pudo extraer texto del PDF")
            return
            
        print(f"✅ Texto extraído ({len(texto)} caracteres)")
        print("\nVista previa del texto extraído:")
        print("-" * 50)
        print(texto[:500] + "..." if len(texto) > 500 else texto)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error al leer el PDF: {e}")
        return

    # 2. Procesamiento con Gemini
    print("\n2️⃣ Procesando con Gemini AI...")
    
    # Cargar configuración
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: No se encontró la API Key de Gemini")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')  # Usando el modelo estable gemini-pro

    # Crear el prompt
    prompt = f"""Eres un experto en extracción de datos de documentos financieros.
A partir del siguiente texto extraído de un documento, necesito que extraigas la siguiente información
y la devuelvas en un formato JSON estricto.

Los campos requeridos son:
{{
    "referencia_unica": string,          // Referencia Única del documento
    "nombre_librado": string,            // Nombre completo del Librado
    "iban": string,                      // Número IBAN, mantener formato
    "importe": float,                    // Cantidad en euros, solo número
    "vencimiento": string,               // Fecha de vencimiento (formato DD/MM/YYYY)
    "emisor": string,                    // Nombre del Emisor
    "identificacion_emisor": string,     // Número o código de identificación del Emisor
    "referencia_fichero": string,        // Referencia del Fichero
    "fecha_recepcion": string,           // Fecha de Recepción (formato DD/MM/YYYY)
    "fecha_documento": string,           // Fecha del Documento (formato DD/MM/YYYY)
    "referencia_documento": string       // Referencia Única del Documento
}}

Reglas importantes:
1. Mantener el formato exacto de fechas como DD/MM/YYYY
2. Para campos no encontrados, usar null (no dejar vacío)
3. Mantener el formato original del IBAN con espacios
4. El importe debe ser un número decimal (sin símbolo €)
5. Devolver SOLO el JSON, sin explicaciones adicionales

Texto del documento a procesar:
{texto}"""

    try:
        # Llamada a Gemini
        respuesta = model.generate_content(prompt)
        
        if not respuesta.text:
            print("❌ Error: Respuesta vacía del modelo")
            return
            
        print("\nRespuesta de Gemini (raw):")
        print("-" * 50)
        print(respuesta.text)
        print("-" * 50)
        
        # Limpiar JSON
        # Buscar contenido entre ```json y ```
        import re
        match = re.search(r"```json\s*([\s\S]*?)\s*```", respuesta.text)
        json_texto = match.group(1) if match else respuesta.text
        json_texto = json_texto.strip()
        
        # Parsear JSON
        datos = json.loads(json_texto)
        print("\n✅ JSON válido obtenido")
        
        # 3. Crear DataFrame y CSV
        print("\n3️⃣ Creando archivo CSV...")
        
        # Crear directorio de salida en la misma carpeta que el PDF
        directorio_salida = os.path.join(os.path.dirname(ruta_pdf), 'output')
        os.makedirs(directorio_salida, exist_ok=True)
        
        # Crear DataFrame
        df = pd.DataFrame([datos])
        
        # Guardar CSV
        nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]
        ruta_salida = os.path.join(directorio_salida, f"{nombre_base}.csv")
        df.to_csv(ruta_salida, index=False, encoding='utf-8')
        
        # Verificar que el archivo se creó
        if os.path.exists(ruta_salida):
            print(f"✅ CSV creado exitosamente en: {ruta_salida}")
            print(f"Tamaño del archivo: {os.path.getsize(ruta_salida)} bytes")
            
            print("\nContenido del CSV:")
            print("-" * 50)
            print(df.to_string())
            print("-" * 50)
        else:
            print(f"❌ Error: No se pudo crear el archivo CSV en {ruta_salida}")
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {str(e)}")
        return

def seleccionar_carpeta():
    """
    Muestra un diálogo para seleccionar una carpeta y retorna la ruta seleccionada.
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con los archivos PDF")
    return carpeta if carpeta else None

def main_test():
    """
    Función principal de prueba
    """
    # Mostrar diálogo para seleccionar carpeta
    directorio_pdfs = seleccionar_carpeta()
    if not directorio_pdfs:
        print("❌ Error: No se seleccionó ninguna carpeta.")
        return
    
    if not os.path.exists(directorio_pdfs):
        print(f"❌ Error: No se encuentra el directorio {directorio_pdfs}")
        return
        
    archivos_pdf = [f for f in os.listdir(directorio_pdfs) if f.lower().endswith('.pdf')]
    
    if not archivos_pdf:
        print(f"❌ No se encontraron archivos PDF en {directorio_pdfs}")
        return
        
    print(f"📁 Se encontraron {len(archivos_pdf)} archivos PDF")
    
    for archivo in archivos_pdf:
        ruta_completa = os.path.join(directorio_pdfs, archivo)
        test_procesamiento_completo(ruta_completa)
        input("\nPresiona Enter para continuar con el siguiente archivo...")

if __name__ == "__main__":
    main_test()