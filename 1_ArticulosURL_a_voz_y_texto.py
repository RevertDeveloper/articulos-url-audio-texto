"""
Este script permite convertir un artículo de una URL a un archivo de audio (mp3) y/o a un archivo de texto (txt).
"""

from newspaper import Article
from gtts import gTTS
import pyttsx3
import os
import validators
from googletrans import Translator
import asyncio
from colorama import init, Fore, Style

# Inicializamos colorama
init(autoreset=True)

IDIOMAS_DISPONIBLES = {
    'es': 'Español',
    'en': 'Inglés',
    'fr': 'Francés',
    'de': 'Alemán',
    'it': 'Italiano',
    # Puedes añadir más idiomas aquí
}

def ajustar_puntuacion(texto):
    # Añadir pausas explícitas en el texto
    texto = texto.replace('. ', '.\n')
    texto = texto.replace(', ', ',\n')
    return texto

async def convertir_texto_a_voz(url, idioma='es', nombre_archivo='articulo', guardar_texto=False, solo_texto=False):
    try:
        # Crear la carpeta si no existe
        if not os.path.exists('articulos_convertidos'):
            os.makedirs('articulos_convertidos')
        
        # Extraemos el articulo
        print(Fore.YELLOW + "📥 Descargando el artículo...")
        article = Article(url)
        article.download()
        article.parse()
        
        # Traducimos el texto al idioma seleccionado
        print(Fore.YELLOW + "🌐 Traduciendo el texto...")
        translator = Translator()
        texto_traducido = await translator.translate(article.text, dest=idioma)
        texto_ajustado = ajustar_puntuacion(texto_traducido.text)
        
        # Guardar el texto traducido si se seleccionó la opción
        if guardar_texto or solo_texto:
            archivo_texto = f'articulos_convertidos/{nombre_archivo}.txt'
            with open(archivo_texto, 'w', encoding='utf-8') as file:
                file.write(texto_ajustado)
            print(Fore.GREEN + f"📄 El archivo de texto '{archivo_texto}' ha sido guardado.")
        
        # Convertimos el texto a voz si no es solo texto
        if not solo_texto:
            print(Fore.YELLOW + "🔊 Convirtiendo el texto a voz...")
            archivo_audio = f'articulos_convertidos/{nombre_archivo}.mp3'
            tts = gTTS(text=texto_ajustado, lang=idioma)
            tts.save(archivo_audio)
            print(Fore.GREEN + f"✅ El archivo de audio '{archivo_audio}' ha sido guardado.")
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")

def menu_interactivo():
    while True:
        print(Fore.CYAN + "\n------- Convertidor de Artículos (en URL) a Voz y Texto --- Traductor a : es/en/fr/de/it ---")
        print(Fore.CYAN + "1.  🎧  Convertir texto de URL a audio (.mp3)")
        print(Fore.CYAN + "2.  📝  Convertir texto de URL a audio y guardar texto (.mp3) y (.txt)")
        print(Fore.CYAN + "3.  📄  Guardar solamente el texto de la URL (.txt)")
        print(Fore.CYAN + "4.  🚪  Salir")
        opcion = input(Fore.CYAN + "Seleccione una opción: ")
        
        if opcion in ['1', '2', '3']:
            url = input(Fore.GREEN + "Ingrese la URL del artículo: ")
            if validators.url(url):
                print(Fore.MAGENTA + "Idiomas disponibles:")
                for codigo, nombre in IDIOMAS_DISPONIBLES.items():
                    print(Fore.MAGENTA + f"{codigo}: {nombre}")
                idioma = input(Fore.BLUE + "Ingrese el código del idioma (por defecto 'es'): ") or 'es'
                if idioma not in IDIOMAS_DISPONIBLES:
                    print(Fore.RED + "Idioma no válido. Usando 'es' por defecto.")
                    idioma = 'es'
                nombre_archivo = input(Fore.BLUE + "Ingrese el nombre del archivo (por defecto 'articulo'): ") or 'articulo'
                guardar_texto = opcion == '2'
                solo_texto = opcion == '3'
                asyncio.run(convertir_texto_a_voz(url, idioma, nombre_archivo, guardar_texto, solo_texto))
            else:
                print(Fore.RED + "URL no válida. Por favor, intente de nuevo.")
        elif opcion == '4':
            print(Fore.CYAN + "Saliendo del programa...")
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    menu_interactivo()