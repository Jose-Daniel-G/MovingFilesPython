import os
import csv
import shutil
import pandas as pd

def verificar_pdfs_en_csv(ruta_carpeta, destino, columna_nombre, cantidad_minima_pdfs=1):
    try:
        archivos = set(os.listdir(ruta_carpeta))
        archivos_csv = {archivo for archivo in archivos if archivo.endswith('.csv')}
        archivos_pdf = {archivo for archivo in archivos if archivo.endswith('.pdf')}
        
        if not archivos_csv:
            print("⚠ No se encontró ningún archivo CSV en la carpeta.")
            return
        
        if len(archivos_pdf) < cantidad_minima_pdfs:
            print(f"⚠ No hay suficientes archivos PDF (mínimo requerido: {cantidad_minima_pdfs}).")
            return
        
        # Usamos el primer archivo CSV encontrado
        archivo_csv = os.path.join(ruta_carpeta, next(iter(archivos_csv))) # NOMBRE CSV
        print(f"📄 Archivo CSV encontrado: {archivo_csv}")
        
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv, dtype=str)

    except Exception as e:
        print(f"❌ Error inesperado al leer el archivo CSV: {e}")
        return

    # Obtener los nombres válidos del CSV
    nombres_validos = set(df[columna_nombre].str.lower().str.strip())

    # Obtener la lista de archivos PDF en la carpeta
    try:
        archivos_pdf = [f for f in os.listdir(ruta_carpeta) if f.endswith('.pdf')]
    except PermissionError:
        print(f"❌ Error: No tienes permisos para acceder a la carpeta: {ruta_carpeta}")
        return
    except FileNotFoundError:
        print(f"❌ Error: La carpeta no existe: {ruta_carpeta}")
        return
    except Exception as e:
        print(f"❌ Error inesperado al leer la carpeta: {e}")
        return

    # Verificar qué archivos PDF no están en el CSV
    pdf_no_encontrados = []
    for pdf in archivos_pdf:
        nombre_pdf_limpio = pdf.replace('.pdf', '').lower().strip()
        if nombre_pdf_limpio not in nombres_validos:
            pdf_no_encontrados.append(pdf)

    # Mostrar resultados
    if pdf_no_encontrados:
        print("⚠ Los siguientes archivos PDF no están en el CSV:")
        for pdf in pdf_no_encontrados:
            print(f" - {pdf}")
    else:
        print("✅ Todos los archivos PDF están en el CSV.")
        
                # Crear la carpeta de destino si no existe
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Mover los archivos PDF
        for pdf in archivos_pdf:
            ruta_origen = os.path.join(ruta_carpeta, pdf)
            ruta_destino = os.path.join(destino, pdf)
            shutil.move(ruta_origen, ruta_destino)
        
        print(f"📂 Todos los archivos PDF han sido movidos a '{destino}'.")
# Ejemplo de uso
ruta_carpeta = "."  # Carpeta donde están los archivos PDF
columna_nombre = "nom_con"  # Nombre de la columna en el CSV que contiene los nombres
destino = "./archivos"  # Reemplázalo con la carpeta donde quieres mover los PDFs

verificar_pdfs_en_csv(ruta_carpeta, destino, columna_nombre,cantidad_minima_pdfs=2)