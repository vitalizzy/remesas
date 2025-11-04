import PyInstaller.__main__
import os
import sys
from pathlib import Path

def create_version_file():
    """Crea el archivo de versión para el ejecutable"""
    version_file = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Lomas Charts'),
        StringStruct(u'FileDescription', u'Extractor de Remesas PDF'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'extractor_remesas'),
        StringStruct(u'LegalCopyright', u'© 2025 Lomas Charts. Todos los derechos reservados.'),
        StringStruct(u'OriginalFilename', u'Extractor_Remesas.exe'),
        StringStruct(u'ProductName', u'Extractor de Remesas'),
        StringStruct(u'ProductVersion', u'1.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open('file_version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_file)

def main():
    # Obtener la ruta absoluta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Crear archivo de versión
    create_version_file()
    
    # Definir los archivos y opciones para PyInstaller
    options = [
        'main.py',  # Script principal
        '--onefile',  # Crear un solo archivo ejecutable
        '--windowed',  # No mostrar la consola en Windows
        '--name', 'Extractor_Remesas',  # Nombre del ejecutable
        '--icon', os.path.join(current_dir, 'resources', 'app_icon.ico'),  # Icono de la aplicación
        '--version-file', 'file_version_info.txt',  # Información de versión
        '--clean',  # Limpiar archivos temporales
        '--noconfirm',  # No preguntar sobre sobreescribir
        '--debug', 'all',  # Mantener logs para debugging
        # Añadir los hooks necesarios para las dependencias
        '--hidden-import', 'google.generativeai',
        '--hidden-import', 'pandas',
        '--hidden-import', 'fitz',
        '--hidden-import', 'python-dotenv',
    ]
    
    # Agregar archivos de datos
    data_files = [
        ('.env', '.'),  # Archivo de configuración
    ]
    
    for src, dst in data_files:
        src_path = os.path.join(current_dir, src)
        if os.path.exists(src_path):
            options.extend(['--add-data', f'{src_path};{dst}'])
    
    try:
        PyInstaller.__main__.run(options)
        print("\n✅ Ejecutable creado exitosamente en la carpeta 'dist'")
        print(f"📁 Ruta: {os.path.join(current_dir, 'dist', 'Extractor_Remesas.exe')}")
    except Exception as e:
        print(f"\n❌ Error al crear el ejecutable: {e}")
        sys.exit(1)
    finally:
        # Limpiar archivo de versión temporal
        if os.path.exists('file_version_info.txt'):
            os.remove('file_version_info.txt')

if __name__ == "__main__":
    main()