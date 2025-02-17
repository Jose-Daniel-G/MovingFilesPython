from flask import Flask, render_template, request
import os
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
        archivos_pdf = {archivo for archivo in archivos if archivo.endswith('.pdf')}

        if not archivos_csv:
            return "⚠ No se encontró ningún archivo CSV en la carpeta."

        archivo_csv = os.path.join(RUTA_CARPETA, next(iter(archivos_csv)))
        df = pd.read_csv(archivo_csv, dtype=str)

    except Exception as e:
        return f"❌ Error al leer el archivo CSV: {e}"

    nombres_validos = {nombre.lower().strip() + ".pdf" for nombre in df[COLUMNA_NOMBRE].dropna()}

    # PDFs que están en la carpeta pero no en el CSV
    pdf_no_encontrados = [pdf for pdf in archivos_pdf if pdf.lower().strip() not in nombres_validos]

    # PDFs que faltan en la carpeta según el CSV
    pdf_faltantes = [pdf for pdf in nombres_validos if pdf not in archivos_pdf]

    # Si hay PDFs no encontrados en el CSV o faltan PDFs, no mover archivos
    if pdf_no_encontrados or pdf_faltantes:
        resultado = "❌ No se moverán los archivos.<br>"
        
        if pdf_no_encontrados:
            resultado += "Los siguientes PDFs no están en el CSV:<br>"
            resultado += "<br>".join(f" - {pdf}" for pdf in pdf_no_encontrados) + "<br><br>"
        
        if pdf_faltantes:
            resultado += "Faltan los siguientes PDFs en la carpeta:<br>"
            resultado += "<br>".join(f" - {pdf}" for pdf in pdf_faltantes)

        return resultado
    else:
        # Si todo está correcto, mover los archivos
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
