import os
from pathlib import Path
import pandas as pd

# Import functions from main.py
import main

def run_headless_test():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    pdf_dir = os.path.join(base_dir, 'my_pdfs')
    if not os.path.exists(pdf_dir):
        print('No se encontró la carpeta my_pdfs')
        return 1

    archivos = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    if not archivos:
        print('No se encontraron PDFs para probar')
        return 1

    # Limitar a 2 PDFs para la prueba rápida
    archivos = archivos[:2]

    directorio_salida = os.path.join(pdf_dir, 'output')
    os.makedirs(directorio_salida, exist_ok=True)

    procesados = []
    # Monkeypatch para evitar llamadas a la API (producción: eliminar/mantener según necesidad)
    sample_tsv = (
        "REF1\tNombre Uno\tES0000000000000000000000\t123.45\t01/01/2025\tEmisorX\tID123\tFileRef\t10/10/2025\t09/10/2025\tDocRef1\n"
        "REF2\tNombre Dos\tES1111111111111111111111\t67.89\t02/02/2025\tEmisorX\tID123\tFileRef\t10/10/2025\t09/10/2025\tDocRef2"
    )
    main.estructurar_informacion_con_gemini = lambda texto: sample_tsv

    for archivo in archivos:
        ruta_pdf = os.path.join(pdf_dir, archivo)
        print(f'Procesando (headless): {archivo}')
        ok = main.procesar_pdf(ruta_pdf, directorio_salida)
        print(f'Resultado: {ok}')
        if ok:
            procesados.append(archivo)

    if not procesados:
        print('Ningún PDF fue procesado correctamente.')
        return 1

    # Ahora combinar usando la misma lógica que main
    dfs = []
    columnas = [
        'Referencia Única', 'Nombre del Librado', 'IBAN', 'Importe', 
        'Vencimiento', 'Emisor', 'Identificación del Emisor', 
        'Referencia del Fichero', 'Fecha de Recepción', 'Fecha del Documento', 
        'Referencia Única del Documento', 'Archivo_Origen'
    ]

    for archivo in procesados:
        nombre_base = os.path.splitext(archivo)[0]
        ruta_tsv = os.path.join(directorio_salida, f"{nombre_base}.tsv")
        if not os.path.exists(ruta_tsv):
            print(f'Archivo esperado no encontrado: {ruta_tsv}')
            continue
        try:
            df = pd.read_csv(ruta_tsv, sep='\t')
            dfs.append(df)
            print(f'Leído: {ruta_tsv} ({len(df)} filas)')
        except Exception as e:
            print(f'Error leyendo {ruta_tsv}: {e}')

    if not dfs:
        print('No hay DataFrames válidos para combinar.')
        return 1

    df_comb = pd.concat(dfs, ignore_index=True)
    ruta_combinado = os.path.join(directorio_salida, 'todos_los_documentos.tsv')
    df_comb.to_csv(ruta_combinado, sep='\t', index=False, encoding='utf-8')

    print('\nResultado combinado:')
    print(f'  Archivos individuales procesados: {len(procesados)}')
    print(f'  Total registros combinados: {len(df_comb)}')
    print('\nEncabezados del TSV combinado:')
    print('\t'.join(df_comb.columns.tolist()))

    # Leer first 5 rows
    print('\nPrimeras 5 filas:')
    print(df_comb.head().to_string())

    # Quick check: ensure header names appear only once in file (no duplicate header lines)
    with open(ruta_combinado, 'r', encoding='utf-8') as f:
        contenido = f.read()
    header_count = contenido.count(df_comb.columns[0])  # count occurrences of first header name
    print(f"\nApariciones del nombre de la primera columna en el archivo combinado: {header_count}")
    # If header_count > number of columns then headers may be duplicated in content; not a perfect check but indicative

    return 0

if __name__ == '__main__':
    exit(run_headless_test())