import os
import pandas as pd

def verificar_pdfs_en_csv(carpeta_pdfs, archivo_csv, columna_nombre):
    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv, dtype=str)
    except PermissionError:
        print(f"❌ Error: No tienes permisos para leer el archivo CSV: {archivo_csv}")
        return
    except FileNotFoundError:
        print(f"❌ Error: El archivo CSV no existe: {archivo_csv}")
        return
    except Exception as e:
        print(f"❌ Error inesperado al leer el archivo CSV: {e}")
        return

    # Obtener los nombres válidos del CSV
    nombres_validos = set(df[columna_nombre].str.lower().str.strip())

    # Obtener la lista de archivos PDF en la carpeta
    try:
        archivos_pdf = [f for f in os.listdir(carpeta_pdfs) if f.endswith('.pdf')]
    except PermissionError:
        print(f"❌ Error: No tienes permisos para acceder a la carpeta: {carpeta_pdfs}")
        return
    except FileNotFoundError:
        print(f"❌ Error: La carpeta no existe: {carpeta_pdfs}")
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

# Ejemplo de uso
carpeta_pdfs = "."  # Carpeta donde están los archivos PDF
archivo_csv = "actividades_transporte.csv"  # Nombre del archivo CSV
columna_nombre = "nom_con"  # Nombre de la columna en el CSV que contiene los nombres

verificar_pdfs_en_csv(carpeta_pdfs, archivo_csv, columna_nombre)