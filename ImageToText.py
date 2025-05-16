!apt-get install -y poppler-utils
!pip install pytesseract pdf2image reportlab
!sudo apt install tesseract-ocr
!sudo apt install libtesseract-dev
!pip install pytesseract
!sudo apt-get install tesseract-ocr-spa

# Importar librerías necesarias
import os
from google.colab import files
from pdf2image import convert_from_path
import pytesseract
from reportlab.pdfgen import canvas

# Seleccionar el archivo PDF de la PC
print("Selecciona el archivo PDF que deseas convertir:")
uploaded = files.upload()

# Tomar el nombre del archivo subido
pdf_filename = list(uploaded.keys())[0]
print("Archivo subido:", pdf_filename)

# Convertir cada página del PDF en una imagen
print("Convirtiendo páginas del PDF en imágenes...")
images = convert_from_path(pdf_filename)

# Configuración del PDF de salida (tamaño A4: 595x842 puntos)
output_pdf_path = "texto_extraido.pdf"
c = canvas.Canvas(output_pdf_path, pagesize=(595, 842))
page_width, page_height = 595, 842

# Configuración para el texto
margin_left = 50
margin_top = 50
line_spacing = 15

# Procesar cada imagen (página) del PDF
print("Realizando OCR y creando PDF de texto plano...")
for idx, image in enumerate(images):
    print("Procesando página {}...".format(idx + 1))
    # Realizar OCR en la imagen (idioma español)
    text = pytesseract.image_to_string(image, lang="spa")

    # Posición inicial para escribir el texto en la página
    y = page_height - margin_top
    for line in text.split("\n"):
        # Verificar si se requiere un salto de página
        if y < margin_top + line_spacing:
            c.showPage()
            y = page_height - margin_top
        c.drawString(margin_left, y, line)
        y -= line_spacing
    # Saltar a una nueva página al finalizar la página actual (opcional)
    c.showPage()

# Guardar el PDF final
c.save()
print("Conversión completada. Revisa el archivo:", output_pdf_path)
