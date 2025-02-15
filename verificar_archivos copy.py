import os
import csv

def verificar_archivos(ruta_carpeta, cantidad_minima_pdfs=1):
    try:
        archivos = set(os.listdir(ruta_carpeta))
    except FileNotFoundError:
        print("La carpeta especificada no existe.")
        return
    
    archivos_csv = {archivo for archivo in archivos if archivo.endswith('.csv')}
    archivos_pdf = {archivo for archivo in archivos if archivo.endswith('.pdf')}
    
    if not archivos_csv:
        print("No se encontró ningún archivo CSV en la carpeta.")
        return
    
    if len(archivos_pdf) < cantidad_minima_pdfs:
        print(f"No hay suficientes archivos PDF (mínimo requerido: {cantidad_minima_pdfs}).")
        return
    
    archivo_csv = os.path.join(ruta_carpeta, next(iter(archivos_csv)))
    nombres_validos = set()
    
    with open(archivo_csv, newline='', encoding='utf-8') as f:
        lector = csv.reader(f)
        nombres_validos = {fila[0].strip().lower() for fila in lector if fila}  # Elimina espacios y convierte a minúsculas
    
    pdf_no_encontrados = [pdf for pdf in archivos_pdf if pdf.lower().replace('.pdf', '').strip() not in nombres_validos]
    
    if pdf_no_encontrados:
        print("Los siguientes archivos PDF no están en el CSV:")
        print("\n".join(f" - {pdf}" for pdf in pdf_no_encontrados))
    else:
        print("Todos los archivos PDF están correctamente listados en el CSV.")

# Uso del programa
directorio = "."  # Cambia por la ruta de tu carpeta
verificar_archivos(directorio, cantidad_minima_pdfs=2)
