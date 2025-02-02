import os
import shutil
from tqdm import tqdm
import zipfile
from typing import List


def list_files(source_dir: str, 
               extensions: tuple[str], 
               include_sub_dir=False) -> List[str]:
    """Varre o diretório e retorna uma lista de arquivos com as extensões especificadas."""
    file_list = []
    
    if include_sub_dir:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(extensions):
                    file_list.append(os.path.join(root, file))
    else:
        for file in os.listdir(source_dir):
            file_path = os.path.join(source_dir, file)
            if os.path.isfile(file_path) and file.endswith(extensions):
                file_list.append(file_path)
    
    return file_list

def move_files(files_to_move: List[str], 
               destination_dir:str,                
               verbose: bool = True):
    """Move todos os arquivos de uma determinada extensão de um diretório para outro."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
   
    for file_path in tqdm(files_to_move, disable=not verbose, desc="Moving files"):
        try:
            shutil.move(file_path, destination_dir)
        except Exception as e:
            print(f"Erro ao mover {file_path}: {e}")
            
def remove_files(file_list: List[str], verbose: bool = True):
    """
    Remove uma lista de arquivos do sistema.

    :param lista_arquivos: Lista contendo os caminhos dos arquivos a serem removidos.
    :param verbose: Se True, mostra o progresso da remoção dos arquivos.
    """
    for arquivo in tqdm(file_list, desc="Removendo arquivos", disable=not verbose):
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"Arquivo removido: {arquivo}")
            except Exception as e:
                print(f"Erro ao remover {arquivo}: {e}")
        else:
            print(f"Arquivo não encontrado: {arquivo}")
            
def copy_files(file_list: List[str], destination_dir: str, prefix: str = "copy_", verbose: bool = True):
    """
    Copia arquivos de uma lista para o diretório de destino.

    :param file_list: Lista de caminhos completos dos arquivos a serem copiados.
    :param destination_dir: Caminho do diretório de destino.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)  # Cria o diretório de destino se não existir
    
    for arquivo in tqdm(file_list, desc="Copiando arquivos", disable=not verbose):
        try:
            if os.path.isfile(arquivo):
                nome_arquivo = os.path.basename(arquivo)  # Obtém o nome do arquivo
                novo_nome = f"{prefix}{nome_arquivo}"  # Adiciona o prefixo ao nome
                caminho_destino = os.path.join(destination_dir, novo_nome)  # Define o caminho de destino
                
                shutil.copy(arquivo, caminho_destino)
            else:
                print(f"Arquivo '{arquivo}' não encontrado ou inválido.")
        except Exception as e:
            print(f"Erro ao copiar '{arquivo}': {e}")

def zip_files(files_to_zip: List[str], 
              output_zip: str,
              verbose: bool = True):
    """
    Compacta uma lista de arquivos em um único arquivo ZIP.
    
    :param files_to_zip: Lista de caminhos dos arquivos a serem compactados.
    :param output_zip: Nome do arquivo ZIP de saída.
    :param verbose: Se True, mostra o progresso da remoção dos arquivos.
    """
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in tqdm(files_to_zip, disable=not verbose, desc="Zipping files"):
            zipf.write(file, arcname=file.split('/')[-1])

def unzip_files(zip_file: str, extract_to: str):
    """
    Extrai um arquivo ZIP para um diretório especificado.
    
    :param zip_file: Arquivo ZIP a ser extraído.
    :param extract_to: Diretório onde os arquivos serão extraídos.
    """
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)  # Cria o diretório de destino se não existir
    
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        zipf.extractall(extract_to)
    print(f"Arquivos extraídos para '{extract_to}' com sucesso!")
    
    
def remove_signature(file_list: List[str], 
                     output_dir: str, 
                     sign_start="|9999|", 
                     encoding="utf-8", 
                     verbose=True):    

    # Processa cada arquivo
    for arquivo in tqdm(file_list, desc="Processando arquivos", disable=not verbose):
        with open(arquivo, "r", encoding=encoding) as arquivo_original:
            linhas = arquivo_original.readlines()
        
        # Encontra a linha que inicia a assinatura digital    
        i = 0
        for linha in linhas:
            if linha.startswith(sign_start):
                break
            else:   
                i+=1
        
        # Remove a assinatura digital apos registro sign_start
        linhas = linhas[:i]

        # Salva o conteúdo modificado em um novo arquivo
        novo_caminho_arquivo = os.path.join(output_dir, f"sem_assinatura_{arquivo}")
        with open(novo_caminho_arquivo, "w", encoding=encoding) as novo_arquivo:
            novo_arquivo.writelines(linhas)
