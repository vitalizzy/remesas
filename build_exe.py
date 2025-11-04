import PyInstaller.__main__
import os
import sys
from pathlib import Path

# Generar icono válido con Pillow para evitar errores de conversión
def create_icon(path_icon: str):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        # Pillow no está disponible; el build fallará más adelante si no existe el icono
        return

    # Crear imagen simple (256x256) con un texto corto
    size = (256, 256)
    img = Image.new('RGBA', size, (40, 120, 200, 255))
    draw = ImageDraw.Draw(img)
    try:
        # Intentar cargar una fuente del sistema, si falla usar la fuente por defecto
        font = ImageFont.truetype('arial.ttf', 80)
    except Exception:
        font = ImageFont.load_default()

    text = "R"
    w, h = draw.textsize(text, font=font)
    draw.text(((size[0]-w)/2, (size[1]-h)/2), text, font=font, fill=(255,255,255,255))

    # Guardar como .ico
    os.makedirs(os.path.dirname(path_icon), exist_ok=True)
    img.save(path_icon, format='ICO')

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
    
    # Asegurarse de tener un icono válido (se generará si falta)
    icon_path = os.path.join(current_dir, 'resources', 'app_icon.ico')
    if not os.path.exists(icon_path):
        print(f"⚙️  No se encontró icono en {icon_path}, generando uno automáticamente...")
        create_icon(icon_path)
    
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
    '--hidden-import', 'dotenv',
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