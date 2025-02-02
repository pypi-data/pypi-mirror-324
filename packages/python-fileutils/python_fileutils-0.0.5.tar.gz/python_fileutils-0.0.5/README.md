# FileUtils - Gerenciamento de Arquivos em Python

Este projeto fornece utilitários para manipulação de arquivos em Python, incluindo listagem, cópia, movimentação, remoção e compactação de arquivos. Além disso, inclui testes unitários para garantir a correta funcionalidade dos métodos implementados.

## 📌 Funcionalidades

O módulo `fileutils.py` contém as seguintes funções:

- **Listagem de arquivos**: `list_files(source_dir, extensions, include_sub_dir=False)`
  - Retorna uma lista de arquivos em um diretório com as extensões especificadas.
  
- **Movimentação de arquivos**: `move_files(files_to_move, destination_dir, verbose=True)`
  - Move arquivos para um diretório de destino.

- **Remoção de arquivos**: `remove_files(file_list, verbose=True)`
  - Remove arquivos do sistema.

- **Cópia de arquivos**: `copy_files(file_list, destination_dir, prefix="copy_", verbose=True)`
  - Copia arquivos para um diretório de destino com um prefixo opcional.

- **Compactação de arquivos**: `zip_files(files_to_zip, output_zip, verbose=True)`
  - Cria um arquivo ZIP contendo os arquivos especificados.

- **Extração de arquivos ZIP**: `unzip_files(zip_file, extract_to)`
  - Extrai arquivos de um ZIP para um diretório específico.

- **Remoção de assinaturas digitais de arquivos**: `remove_signature(file_list, output_dir, sign_start="|9999|", encoding="utf-8", verbose=True)`
  - Remove assinaturas digitais de arquivos a partir de um marcador específico.

- **Organização de arquivos**: `organize(source_dir, destination_dir, file_selector=default_file_selector, copy=True, verbose=True)`
  - Organiza arquivos conforme um função seletora e move ou copia para um diretório específico.

## 🧪 Testes Unitários

O projeto inclui testes unitários para validar a funcionalidade das funções. Os testes são implementados nos seguintes arquivos:

- `01_list_files_test.py`: Testa a listagem de arquivos no diretório.
- `02_copy_files_test.py`: Testa a cópia de arquivos para um diretório de destino.
- `03_unzip_files_test.py`: Testa a extração de arquivos ZIP.
- `04_zip_file_test.py`: Testa a criação de arquivos ZIP.
- `05_organize_test.py`: Testa a organização de arquivos para um diretório de destino.

Os testes utilizam `unittest` e podem ser executados com:

```sh
python -m unittest discover
```

## 🚀 Como Usar

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/fileutils.git
   cd fileutils
   ```

2. Instale as dependências:
   ```sh
   pip install tqdm
   ```

3. Utilize os métodos diretamente no seu código Python, por exemplo:

   ```python
   from fileutils import list_files, copy_files

   arquivos = list_files(source_dir="meu_diretorio", extensions=(".txt", ".csv"))
   copy_files(arquivos, destination_dir="backup")
   ```

4. Execute os testes para verificar a integridade do código:
   ```sh
   python -m unittest discover
   ```

## 📜 Licença

Este projeto está sob a licença MIT.
