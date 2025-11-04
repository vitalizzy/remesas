import os
import fitz  # PyMuPDF
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from io import StringIO
import re
import tkinter as tk
from tkinter import filedialog

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
    # Nota: 'gemini-2.5-flash' no es un modelo válido actualmente. Usamos 'gemini-1.5-flash'.
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
8.  La columna Importe debe conservar la separacion decimal tal y como se muestra en el documento.
9.  No hagas comentarios adicionales, devuelve solo el TSV.

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

def procesar_pdf(ruta_pdf: str, directorio_salida: str) -> bool:
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
        
        # Agregar la columna con el nombre del archivo origen
        nombre_archivo = os.path.basename(ruta_pdf)
        df['Archivo_Origen'] = nombre_archivo
        
        # Asegurarse de que el directorio de salida existe
        os.makedirs(directorio_salida, exist_ok=True)
        
        nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]
        ruta_salida = os.path.join(directorio_salida, f"{nombre_base}.tsv")
        
        df.to_csv(ruta_salida, sep='\t', index=False, encoding='utf-8')
        
        print(f"✅ TSV creado exitosamente en: {ruta_salida}")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear el archivo TSV: {str(e)}")
        print("--- Datos recibidos de Gemini ---")
        print(datos_tsv)
        print("---------------------------------")
        return False

def seleccionar_carpeta():
    """
    Muestra un diálogo para seleccionar una carpeta y retorna la ruta seleccionada.
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con los archivos PDF")
    return carpeta if carpeta else None

def main():
    """
    Función principal que procesa todos los PDFs en el directorio seleccionado.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Error: No se encontró la variable de entorno GOOGLE_API_KEY en el archivo .env")
        return
    genai.configure(api_key=api_key)
    print("✓ API Key de Google configurada.")
    
    # Mostrar diálogo para seleccionar carpeta
    directorio_pdfs = seleccionar_carpeta()
    if not directorio_pdfs:
        print("❌ Error: No se seleccionó ninguna carpeta.")
        return
    
    if not os.path.exists(directorio_pdfs):
        print(f"❌ Error: El directorio '{directorio_pdfs}' no existe.")
        return
        
    archivos_pdf = [f for f in os.listdir(directorio_pdfs) if f.lower().endswith('.pdf')]
    if not archivos_pdf:
        print(f"ℹ️ No se encontraron archivos PDF en el directorio '{directorio_pdfs}'.")
        return
        
    print(f"📁 Encontrados {len(archivos_pdf)} PDF(s) para procesar.")
    
    # Procesar cada PDF y mantener un registro de los archivos procesados exitosamente
    # Crear el directorio de salida dentro de la carpeta seleccionada
    directorio_salida = os.path.join(directorio_pdfs, 'output')
    os.makedirs(directorio_salida, exist_ok=True)

    archivos_procesados = []
    for archivo in archivos_pdf:
        ruta_completa = os.path.join(directorio_pdfs, archivo)
        if procesar_pdf(ruta_completa, directorio_salida):
            archivos_procesados.append(archivo)
    
    # Combinar todos los TSV procesados en un solo archivo
    if archivos_procesados:
        print("\n=== Combinando archivos TSV ===")
        dfs = []
        for archivo in archivos_procesados:
            nombre_base = os.path.splitext(archivo)[0]
            ruta_tsv = os.path.join(directorio_salida, f"{nombre_base}.tsv")
            try:
                # Leer el TSV sin encabezados y agregar la columna con el nombre del PDF
                columnas = [
                    'Referencia Única', 'Nombre del Librado', 'IBAN', 'Importe', 
                    'Vencimiento', 'Emisor', 'Identificación del Emisor', 
                    'Referencia del Fichero', 'Fecha de Recepción', 'Fecha del Documento', 
                    'Referencia Única del Documento', 'Archivo_Origen'
                ]
                df = pd.read_csv(ruta_tsv, sep='\t', names=columnas, skiprows=1)  # Saltamos la primera fila (encabezados)
                dfs.append(df)
                print(f"✓ Leído: {archivo}")
            except Exception as e:
                print(f"❌ Error al leer {archivo}: {e}")
        
        if dfs:
            # Combinar todos los DataFrames
            df_combinado = pd.concat(dfs, ignore_index=True)
            
            # Guardar el archivo combinado
            ruta_combinado = os.path.join(directorio_salida, "todos_los_documentos.tsv")
            df_combinado.to_csv(ruta_combinado, sep='\t', index=False, encoding='utf-8')
            print(f"\n✅ Archivo combinado creado en: {ruta_combinado}")
            print(f"   Total de registros: {len(df_combinado)}")
    
    print("\n=== Resumen del Procesamiento ===")
    print(f"Total de archivos: {len(archivos_pdf)}")
    print(f"✅ Procesados exitosamente: {len(archivos_procesados)}")
    print(f"❌ Fallidos: {len(archivos_pdf) - len(archivos_procesados)}")

if __name__ == "__main__":
    main()