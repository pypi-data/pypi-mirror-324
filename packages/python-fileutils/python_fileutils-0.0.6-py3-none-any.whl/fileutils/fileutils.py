import os
import shutil
from tqdm import tqdm
import zipfile
from typing import List, Dict
from typing import Callable


def list_files(source_dir: str, 
               extensions: tuple[str], 
               include_sub_dir=False,
               verbose=False,
               verbose_text="Buscando arquivos") -> List[str]:
    """Varre o diretório e retorna uma lista de arquivos com as extensões especificadas."""
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Diretório não encontrado: {source_dir}")
    
    file_list = []
    
    if include_sub_dir:
        for root, _, files in tqdm(os.walk(source_dir), desc=verbose_text, disable=not verbose):
            for file in files:
                if file.endswith(extensions):
                    file_list.append(os.path.join(root, file))
    else:
        for file in tqdm(os.listdir(source_dir), desc=verbose_text, disable=not verbose):
            file_path = os.path.join(source_dir, file)
            if os.path.isfile(file_path) and file.endswith(extensions) or extensions == ("*"):
                file_list.append(file_path)
    
    return file_list

def move_files(files_to_move: List[str], 
               destination_dir:str,                
               verbose: bool = False,
               verbose_text="Movendo arquivos"):
    """Move todos os arquivos de uma determinada extensão de um diretório para outro."""
    
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
   
    for file_path in tqdm(files_to_move, disable=not verbose, desc=verbose_text):
        try:
            shutil.move(file_path, destination_dir)
        except Exception as e:
            raise RuntimeError(f"Erro ao mover {file_path}: {e}")
            
def remove_files(file_list: List[str], 
                 verbose: bool = True, 
                 verbose_text="Removendo arquivos"):
    """
    Remove uma lista de arquivos do sistema.

    :param lista_arquivos: Lista contendo os caminhos dos arquivos a serem removidos.
    :param verbose: Se True, mostra o progresso da remoção dos arquivos.
    """
    for arquivo in tqdm(file_list, desc=verbose_text, disable=not verbose):
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
            except Exception as e:
                raise RuntimeError(f"Erro ao remover {arquivo}: {e}")
        else:
           raise FileNotFoundError(f"Arquivo '{arquivo}' nao encontrado.")
            
def copy_files(file_list: List[str], 
               destination_dir: str, 
               prefix: str = "copy_", 
               verbose: bool = False,
               verbose_text="Copiando arquivos"):
    """
    Copia arquivos de uma lista para o diretório de destino.

    :param file_list: Lista de caminhos completos dos arquivos a serem copiados.
    :param destination_dir: Caminho do diretório de destino.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)  # Cria o diretório de destino se não existir
    
    for file_path in tqdm(file_list, desc=verbose_text, disable=not verbose):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado ou inválido: {file_path}")
        try:
            nome_arquivo = os.path.basename(file_path)  # Obtém o nome do arquivo
            novo_nome = f"{prefix}{nome_arquivo}"  # Adiciona o prefixo ao nome
            caminho_destino = os.path.join(destination_dir, novo_nome)  # Define o caminho de destino                
            shutil.copy(file_path, caminho_destino)
        except Exception as e:
            raise RuntimeError(f"Erro ao copiar '{file_path}': {e}")

def zip_files(files_to_zip: List[str], 
              output_zip: str,
              verbose: bool = False,
              verbose_text="Compactando arquivos"):
    """
    Compacta uma lista de arquivos em um único arquivo ZIP.
    
    :param files_to_zip: Lista de caminhos dos arquivos a serem compactados.
    :param output_zip: Nome do arquivo ZIP de saída.
    :param verbose: Se True, mostra o progresso da remoção dos arquivos.
    """
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in tqdm(files_to_zip, desc=verbose_text, disable=not verbose):
                zipf.write(file, arcname=os.path.basename(file))
    except Exception as e:
        raise RuntimeError(f"Erro ao compactar arquivos: {e}")

def unzip_files(zip_file: str, extract_to: str):
    """
    Extrai um arquivo ZIP para um diretório especificado.
    
    :param zip_file: Arquivo ZIP a ser extraído.
    :param extract_to: Diretório onde os arquivos serão extraídos.
    """
    """Extrai arquivos de um ZIP."""
    if not os.path.exists(zip_file):
        raise FileNotFoundError(f"Arquivo ZIP não encontrado: {zip_file}")
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    try:
        with zipfile.ZipFile(zip_file, 'r') as zipf:
            zipf.extractall(extract_to)
    except Exception as e:
        raise RuntimeError(f"Erro ao extrair arquivos do ZIP: {e}")
    
    
def remove_signature(file_list: List[str], 
                     output_dir: str, 
                     sign_start="|9999|", 
                     encoding="utf-8", 
                     verbose=False,
                     verbose_text="Removendo assinatura digital"):    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Processa cada arquivo
    for arquivo in tqdm(file_list, desc=verbose_text, disable=not verbose):
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
        novo_caminho_arquivo = os.path.join(output_dir, f"sem_assinatura_{os.path.basename(arquivo)}")
        with open(novo_caminho_arquivo, "w", encoding=encoding) as novo_arquivo:
            novo_arquivo.writelines(linhas)

def default_file_selector(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".txt", ".md"]:
        return "text_files"
    elif ext in [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".tiff"]:
        return "images"
    elif ext in [".csv", ".xlsx", ".xls"]:
        return "data_files"
    elif ext in [".pdf", ".docx", ".doc", ".rtf"]:
        return "documents"
    elif ext in [".zip", ".rar", ".7z"]:
        return "compressed_files"
    elif ext in [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"]:
        return "video_files"
    elif ext in [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"]:
        return "audio_files"
    elif ext in [".bat", ".cmd", ".ps1", ".sh"]:
        return "scripts"
    elif ext in [".xml", ".html", ".css", ".js", ".json"]:
        return "web_files"
    elif ext in [".py", ".ipynb"]:
        return "python_files"
    else:
        return "others" 

def organize_files(source_dir: str, 
                   destination_dir: str,
                   file_selector: Callable[[str], str] = default_file_selector, 
                   copy=False,
                   include_sub_dir=False, 
                   verbose=False):
    """
    Organiza arquivos de uma pasta e subpastas, movendo ou copiando conforme a lógica definida na função `file_selector`.

    :param source_dir: Diretório de origem.
    :param file_selector: Função que recebe o caminho do arquivo e retorna o nome da pasta de destino. Se retornar None, o arquivo será ignorado.
    :param destination_dir: Diretório de destino.
    :param copy: Se True, copia os arquivos ao invés de movê-los.
    :param include_sub_dir: Se True, inclui os arquivos de subpastas.
    :param verbose: Se True, mostra o progresso da remoção dos arquivos.
    """
    
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"O diretório de origem '{source_dir}' nao foi encontrado.")
    
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    files = list_files(source_dir, ("*"), include_sub_dir=include_sub_dir)
    files_dict = {}
        
    for file_path in tqdm(files, desc="Separando arquivos", disable=not verbose):        
        dest_dir = file_selector(file_path)
        file_list = files_dict.get(dest_dir, [])
        file_list.append(file_path)
        files_dict[dest_dir] = file_list
    
    for dest_dir, file_list in tqdm(files_dict.items(), desc="Organizando arquivos em pastas", disable=not verbose):
        if copy:
            copy_files(file_list, f'{destination_dir}/{dest_dir}')
        else:
            move_files(file_list, f'{destination_dir}/{dest_dir}')   