import os
from PIL import Image, ExifTags
import utm
import requests
import time

# Configurações
EXTENSOES_ACEITAS = ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG']
API_URL = "https://nominatim.openstreetmap.org/reverse"
HEADERS = {"User-Agent": "ExtratorDeCoordenadas/1.0"}

# converte coordenadas de graus, minutos e segundos para graus decimais.
def converte_graus_decimais(direcao, coord):
    graus = coord[0].numerator / coord[0].denominator
    minutos = coord[1].numerator / coord[1].denominator
    segundos = coord[2].numerator / coord[2].denominator
    
    coordenada = graus + minutos / 60 + segundos / 3600

    if direcao in ['S', 'W']:
        coordenada = coordenada * (-1)

    return coordenada

#obtém informações detalhadas da localização a partir da latitude e longitude.
def obter_endereco(lat, lon):
    try:
        params = {"lat": lat, "lon": lon, "format": "json"}
        response = requests.get(API_URL, headers=HEADERS, params=params)
        response.raise_for_status()  # Levanta uma exceção para erros HTTP
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter endereço: {e}")
        return None

#Extrai coordenadas GPS de uma imagem e converte para graus decimais e UTM.
def extrair_coordenadas(arq):
    try:
        with Image.open(arq) as foto:
            exif_data = foto._getexif()
            
            if 34853 in exif_data:  # Verifica se a imagem contém metadados GPS
                info = exif_data[34853]
                
                lat = converte_graus_decimais(info[1], info[2])
                lon = converte_graus_decimais(info[3], info[4])
                
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    print(f"\nCoordenadas GPS encontradas: Latitude = {lat}, Longitude = {lon}")
                    
                    # converte as coordenadas para UTM
                    utm_x, utm_y, fuso, letra = utm.from_latlon(lat, lon)
                    fuso_letra = str(fuso) + letra
                    
                    # obtém informações detalhadas da localização
                    endereco = obter_endereco(lat, lon)
                    if endereco:
                        print("\nInformações detalhadas da localização:")
                        print(f"Endereço: {endereco.get('display_name', 'N/A')}")
                        print(f"CEP: {endereco.get('address', {}).get('postcode', 'N/A')}")
                        print(f"Cidade: {endereco.get('address', {}).get('city', 'N/A')}")
                        print(f"Estado: {endereco.get('address', {}).get('state', 'N/A')}")
                        print(f"País: {endereco.get('address', {}).get('country', 'N/A')}")
                    else:
                        print("\nNenhuma informação de localização encontrada.")
                else:
                    print("\nCoordenadas GPS inválidas.")
                
            else:
                print("\nNenhuma coordenada GPS encontrada.")

            print('-=' * 60)
    except Exception as e:
        print(f"Erro ao processar {arq}: {e}")

def print_metadados(filepath):
    try:
        with Image.open(filepath) as image: 
            exif_data = image._getexif() # Metadados EXIF
            
            # exibe os metadados EXIF, se existirem
            if exif_data is not None:
                print("\nMetadados EXIF:")
                for tag, value in exif_data.items():
                    tagname = ExifTags.TAGS.get(tag, tag) # converte o código da tag para o nome legível
                    print(f"{tagname}: {value}") # exibe os dados no terminal
            else:
                print("\nEsta imagem não contém metadados EXIF.")
            
    except FileNotFoundError:
        print(f"\nErro: O arquivo '{filepath}' não foi encontrado.")
    except Exception as e:
        print(f"\nErro ao processar a imagem: {e}")

#Processa todas as imagens na pasta atual e exibe as coordenadas e metadados.
def main():
    fotos = []
    
     # Percorre todos os arquivos no diretório atual
    for nome in os.listdir('.'):
        # Verifica se o arquivo tem uma extensão válida
        for ext in EXTENSOES_ACEITAS:
            if nome.endswith(ext):
                fotos.append(nome)  # Adiciona o nome do arquivo à lista
                break  # Sai do loop interno após encontrar uma extensão válida

    for nome in fotos:
        print(f"\nProcessando {nome}...")
        print_metadados(nome) # Exibe os metadados da imagem
        extrair_coordenadas(nome) # extrai e exibe as coordenadas
        time.sleep(1)  # delay para evitar bloqueios na API

main()