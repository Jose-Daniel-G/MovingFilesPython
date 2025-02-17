from flask import Flask, render_template, request
import os
import csv
import shutil
import pandas as pd

app = Flask(__name__)

# Configuración de rutas
RUTA_CARPETA = "./Conceptos Varios"
DESTINO = "./Conceptos Varios/archivos"
COLUMNA_NOMBRE = "nom_con"

def verificar_pdfs_en_csv():
    try:
        archivos = set(os.listdir(RUTA_CARPETA))
        archivos_csv = {archivo for archivo in archivos if archivo.endswith('.csv')}
        archivos_pdf = {pdf.lower().strip() for pdf in os.listdir(RUTA_CARPETA) if pdf.endswith('.pdf')}
        # archivos_pdf = {archivo for archivo in archivos if archivo.endswith('.pdf')}

        if not archivos_csv:
            return "⚠ No se encontró ningún archivo CSV en la carpeta."
        elif len(archivos_csv) > 1: 
            return "⚠ Solo debe haber un archivo CSV en la carpeta."

        if len(archivos_pdf) < 1:
            return "⚠ No hay suficientes archivos PDF."

        archivo_csv = os.path.join(RUTA_CARPETA, next(iter(archivos_csv)))
        df = pd.read_csv(archivo_csv, dtype=str)

    except Exception as e:
        return f"❌ Error al leer el archivo CSV: {e}"

    nombres_validos = set(df[COLUMNA_NOMBRE].str.lower().str.strip())

    # Comparar nombres y detectar faltantes
    pdfs_faltantes = {nombre for nombre in nombres_validos if f"{nombre}.pdf" not in archivos_pdf}
    
    # Comparar si existen en el csv
    pdf_no_encontrados = [pdf for pdf in archivos_pdf if pdf.replace('.pdf', '').lower().strip() not in nombres_validos]
          
    if pdf_no_encontrados:
        resultado = "❌ No se moverán los archivos. Los siguientes PDFs no están en el CSV:<br>"
        resultado += "<br>".join(f" - {pdf}" for pdf in pdf_no_encontrados)
        return resultado
    
    elif pdfs_faltantes:
        # Imprimir los faltantes
        resultado = "\n📂No se moverán los archivos. Ya que faltan los siguientes PDFs:<br>"
        resultado += "<br>".join(f" - {pdf}" for pdf in pdfs_faltantes)   
        return resultado
    
    else:
        if not os.path.exists(DESTINO):
            os.makedirs(DESTINO)

        for pdf in archivos_pdf:
            shutil.move(os.path.join(RUTA_CARPETA, pdf), os.path.join(DESTINO, pdf))

        return "✅ Todos los archivos PDF fueron movidos correctamente."

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""
    if request.method == "POST":
        resultado = verificar_pdfs_en_csv()
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
