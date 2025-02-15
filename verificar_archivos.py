import os
import csv
import shutil

def limpiar_nombre(nombre):
    """Limpia el nombre eliminando espacios extra y convirtiéndolo a minúsculas."""
    return nombre.lower().strip()

def verificar_archivos(ruta_carpeta, destino, cantidad_minima_pdfs=1):
    try:
        archivos = set(os.listdir(ruta_carpeta))
    except FileNotFoundError:
        print("❌ La carpeta especificada no existe.")
        return
    
    archivos_csv = {archivo for archivo in archivos if archivo.endswith('.csv')}
    archivos_pdf = {archivo for archivo in archivos if archivo.endswith('.pdf')}
    
    if not archivos_csv:
        print("⚠ No se encontró ningún archivo CSV en la carpeta.")
        return
    
    if len(archivos_pdf) < cantidad_minima_pdfs:
        print(f"⚠ No hay suficientes archivos PDF (mínimo requerido: {cantidad_minima_pdfs}).")
        return
    
    # Usamos el primer archivo CSV encontrado
    archivo_csv = os.path.join(ruta_carpeta, next(iter(archivos_csv)))
    
    nombres_validos = set()
    
    with open(archivo_csv, newline='', encoding='utf-8') as f:
        lector = csv.reader(f)
        nombres_validos = {limpiar_nombre(fila[0]) for fila in lector if fila}  # Limpiamos nombres
    
    # Verificamos los PDFs contra los nombres del CSV
    pdf_no_encontrados = [
        pdf for pdf in archivos_pdf 
        if limpiar_nombre(pdf.replace('.pdf', '')) not in nombres_validos
    ]
    
    if not pdf_no_encontrados:
        print(f"⚠ Los siguientes archivos PDF NO están en el CSV (total: {len(pdf_no_encontrados)}):")
        print("\n".join(f" - {pdf}" for pdf in pdf_no_encontrados))
    else:
        print("✅ Todos los archivos PDF están correctamente listados en el CSV.")
        
        # Crear la carpeta de destino si no existe
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Mover los archivos PDF
        for pdf in archivos_pdf:
            ruta_origen = os.path.join(ruta_carpeta, pdf)
            ruta_destino = os.path.join(destino, pdf)
            shutil.move(ruta_origen, ruta_destino)
        
        print(f"📂 Todos los archivos PDF han sido movidos a '{destino}'.")

# 🚀 **Ejemplo de uso**
directorio = "."  # Reemplázalo con la carpeta donde están los archivos
destino = "./archivos"  # Reemplázalo con la carpeta donde quieres mover los PDFs

verificar_archivos(directorio, destino, cantidad_minima_pdfs=2)
