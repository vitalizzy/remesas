import os
import fitz  # PyMuPDF

def probar_extraccion_pdf(ruta_pdf: str) -> str:
    """
    Prueba la extracción de texto de un PDF y muestra información detallada.
    """
    print(f"\n=== Prueba de Extracción de PDF ===")
    print(f"Archivo: {os.path.basename(ruta_pdf)}")
    print("-" * 50)
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(ruta_pdf):
            
            print(f"❌ Error: El archivo no existe en {ruta_pdf}")
            return None
            
        # Intentar abrir el PDF
        documento = fitz.open(ruta_pdf)
        print(f"\n📄 Información del PDF:")
        print(f"Número de páginas: {len(documento)}")
        print(f"Tamaño del archivo: {os.path.getsize(ruta_pdf) / 1024:.2f} KB")
        
        texto_completo = ""
        for num_pagina, pagina in enumerate(documento, 1):
            print(f"\nProcesando página {num_pagina}:")
            texto_pagina = pagina.get_text()
            
            # Información sobre la página
            palabras = len(texto_pagina.split())
            caracteres = len(texto_pagina)
            
            if texto_pagina.strip():
                print(f"✓ Encontrados {palabras} palabras, {caracteres} caracteres")
                # Mostrar una vista previa del texto
                preview = texto_pagina.strip()[:150]
                print(f"Vista previa: {preview}...")
                texto_completo += texto_pagina
            else:
                print(f"⚠️  No se encontró texto en esta página")
        
        documento.close()
        
        # Resumen final
        total_palabras = len(texto_completo.split())
        total_caracteres = len(texto_completo)
        
        print(f"\n=== Resumen de la Extracción ===")
        print(f"Total de palabras: {total_palabras}")
        print(f"Total de caracteres: {total_caracteres}")
        
        if not texto_completo.strip():
            print("❌ Advertencia: No se encontró texto en ninguna página")
            return None
            
        return texto_completo
        
    except Exception as e:
        print(f"❌ Error al procesar el PDF: {str(e)}")
        return None

def seleccionar_carpeta():
    """
    Muestra un diálogo para seleccionar una carpeta y retorna la ruta seleccionada.
    """
    import tkinter as tk
    from tkinter import filedialog
    
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta con los archivos PDF")
    return carpeta if carpeta else None

def main_prueba():
    """
    Función principal para probar la extracción de PDFs
    """
    # Mostrar diálogo para seleccionar carpeta
    directorio_pdfs = seleccionar_carpeta()
    if not directorio_pdfs:
        print("❌ Error: No se seleccionó ninguna carpeta.")
        return
    
    if not os.path.exists(directorio_pdfs):
        print(f"❌ Error: No se encuentra el directorio {directorio_pdfs}")
        return
        
    # Obtener lista de PDFs
    archivos_pdf = [f for f in os.listdir(directorio_pdfs) if f.lower().endswith('.pdf')]
    
    if not archivos_pdf:
        print(f"❌ No se encontraron archivos PDF en {directorio_pdfs}")
        return
        
    print(f"📁 Se encontraron {len(archivos_pdf)} archivos PDF")
    
    # Procesar cada PDF
    for archivo in archivos_pdf:
        ruta_completa = os.path.join(directorio_pdfs, archivo)
        texto = probar_extraccion_pdf(ruta_completa)
        
        if texto:
            print(f"\n✅ Extracción exitosa para {archivo}")
        else:
            print(f"\n❌ Falló la extracción para {archivo}")
            
        input("\nPresiona Enter para continuar con el siguiente archivo...")

if __name__ == "__main__":
    main_prueba()