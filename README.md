# Extrator de Metadados e Coordenadas GPS

Este script extrai metadados EXIF e coordenadas GPS de imagens (JPG, PNG, etc.) e exibe informações detalhadas da localização usando a API do OpenStreetMap.


---

### 🛠 Funcionalidades

    Extrai metadados EXIF de imagens.

    Converte coordenadas GPS (graus, minutos, segundos) para graus decimais.

    Converte coordenadas GPS para o sistema UTM.

    Obtém informações detalhadas da localização (endereço, CEP, cidade, estado, país) usando a API do OpenStreetMap.

## 🚀 Como Usar

### Pré-requisitos
- Python 3.x instalado.
- Bibliotecas necessárias: `Pillow`, `requests`, `utm`.


### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/Jaiir0/FotoLocalizador.git
   cd FotoLocalizador
   
2. Instale as dependências:
   pip install -r requirements.txt

4. Executando o Script

    Coloque as imagens que deseja processar na raiz do projeto.
    Execute o script:
    python Metadados_GPS.py

### 📄 Exemplo de Saída

Ao processar uma imagem, o script exibe algo como:

Processando foto.jpg...

Metadados EXIF:
Make: Canon
Model: EOS 5D Mark IV
GPSInfo: Disponível

Coordenadas GPS encontradas: Latitude = -12.5005, Longitude = -24.5321

Informações detalhadas da localização:
Endereço: Avenida Paulista, São Paulo, SP, Brasil
CEP: 01110-100
Cidade: São Paulo
Estado: São Paulo
País: Brasil

### 📝 Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo LICENSE para mais detalhes.
