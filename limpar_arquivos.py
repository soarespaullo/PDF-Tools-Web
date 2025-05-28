import os  # Importa o módulo para manipulação de arquivos e diretórios
import time  # Importa o módulo para lidar com tempo e datas

# Definição das pastas onde os arquivos temporários estão armazenados
UPLOAD_FOLDER = "/var/www/PDFTools/uploads"
RESULT_FOLDER = "/var/www/PDFTools/results"

# Tempo limite para exclusão (10 minutos)
TEMPO_LIMITE = 10 * 60  # Converte 10 minutos para segundos (600 segundos)

def limpar_pasta(pasta):
    """Função para limpar arquivos antigos de uma pasta"""
    
    agora = time.time()  # Obtém o timestamp atual

    # Percorre todos os arquivos dentro da pasta especificada
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)  # Gera o caminho completo do arquivo
        
        if os.path.isfile(caminho):  # Verifica se o item é um arquivo
            tempo_modificacao = os.path.getmtime(caminho)  # Obtém o timestamp da última modificação do arquivo

            # Se o arquivo for mais antigo do que o tempo limite definido, ele será removido
            if agora - tempo_modificacao > TEMPO_LIMITE:
                os.remove(caminho)  # Apaga o arquivo
                print(f"🗑️ Arquivo removido: {caminho}")  # Exibe uma mensagem no terminal indicando a remoção

# Executa a limpeza nas pastas especificadas
limpar_pasta(UPLOAD_FOLDER)
limpar_pasta(RESULT_FOLDER)
