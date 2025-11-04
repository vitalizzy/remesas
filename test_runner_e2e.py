import os
from pathlib import Path
import pandas as pd
import time

# Import functions from main.py
import main

def run_e2e_test():
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
    for archivo in archivos:
        ruta_pdf = os.path.join(pdf_dir, archivo)
        print(f'=== E2E Procesando: {archivo} ===')
        start = time.time()
        ok = main.procesar_pdf(ruta_pdf, directorio_salida)
        elapsed = time.time() - start
        print(f'Tiempo: {elapsed:.1f}s - Resultado: {ok}\n')
        if ok:
            procesados.append(archivo)

    if not procesados:
        print('Ningún PDF fue procesado correctamente en E2E.')
        return 1

    # Combinar usando la misma lógica que main
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
        print('No hay DataFrames válidos para combinar en E2E.')
        return 1

    df_comb = pd.concat(dfs, ignore_index=True)
    ruta_combinado = os.path.join(directorio_salida, 'todos_los_documentos_e2e.tsv')
    df_comb.to_csv(ruta_combinado, sep='\t', index=False, encoding='utf-8')

    print('\n=== Resultado combinado E2E ===')
    print(f'  Archivos individuales procesados: {len(procesados)}')
    print(f'  Total registros combinados: {len(df_comb)}')
    print('\nEncabezados del TSV combinado:')
    print('\t'.join(df_comb.columns.tolist()))

    # Check exact header duplication: count lines equal to header
    with open(ruta_combinado, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    header = '\t'.join(df_comb.columns.tolist()).strip() + '\n'
    header_lines = sum(1 for l in lines if l == header)
    print(f"\nVeces que la línea de cabecera exacta aparece en el archivo combinado: {header_lines}")

    print('\nPrimeras 5 filas:')
    print(df_comb.head().to_string())

    return 0

if __name__ == '__main__':
    exit(run_e2e_test())