import re
from google.colab import files

# Función para limpiar texto
def limpiar_texto(texto):
    # Eliminar múltiples espacios (más de uno) y reemplazarlos por un solo espacio
    texto = re.sub(r'\s+', ' ', texto)

    # Eliminar espacios antes y después de las líneas
    texto = texto.strip()

    return texto

# Función para eliminar líneas que contienen palabras específicas
def eliminar_lineas_con_palabras(texto, palabras):
    # Convertimos el texto en una lista de líneas
    lineas = texto.split('\n')

    # Filtramos las líneas que no contienen las palabras no deseadas
    lineas_filtradas = [linea for linea in lineas if not any(palabra in linea for palabra in palabras)]

    # Volvemos a juntar las líneas filtradas en un solo texto
    texto_filtrado = '\n'.join(lineas_filtradas)

    return texto_filtrado

# Función principal para procesar el archivo
def procesar_archivo(path_archivo, palabras_no_deseadas):
    # Abrir el archivo .txt
    with open(path_archivo, 'r', encoding='utf-8') as archivo:
        texto = archivo.read()

    # Limpiar el texto
    texto_limpio = limpiar_texto(texto)

    # Eliminar líneas con palabras específicas
    texto_filtrado = eliminar_lineas_con_palabras(texto_limpio, palabras_no_deseadas)

    # Asegurarnos de que el texto esté limpio y listo para TTS
    texto_final = limpiar_texto(texto_filtrado)

    return texto_final

# Función para verificar que el texto esté limpio
def verificar_texto(texto):
    # Comprobamos que no haya espacios múltiples, líneas vacías ni palabras innecesarias
    if len(re.findall(r'\s{2,}', texto)) > 0:  # Busca más de un espacio consecutivo
        print("El texto aún contiene múltiples espacios.")
        return False

    if texto == "":
        print("El texto está vacío.")
        return False

    print("El texto está limpio y listo para usar.")
    return True

# Subir archivo a Google Colab
uploaded = files.upload()

# Obtener el nombre del archivo subido
path_archivo = next(iter(uploaded))  # Obtiene el nombre del archivo subido

# Lista de palabras a eliminar
palabras_no_deseadas = [' Fernando Pedrosa, Florencia Deich, Cecilia Noce (compiladores)', 'Herramientas para el análisis de la sociedad y el Estado']  # Lista de palabras a eliminar

# Procesar el archivo
texto_resultante = procesar_archivo(path_archivo, palabras_no_deseadas)

# Verificar el texto
if verificar_texto(texto_resultante):
    print("Texto limpio y listo para ser usado en TTS:")
    print(texto_resultante)
else:
    print("Hubo un problema con el texto.")