import os
import json
from PyPDF2 import PdfReader

# Obtém o diretório atual do arquivo em execução
base_dir = os.path.dirname(os.path.abspath(__file__))

# Extrai o diretório pai do diretório atual
parent_dir = os.path.dirname(base_dir)

# Cria o caminho para o diretório que contém os arquivos PDF
pdf_dir = os.path.join(parent_dir, 'extract', 'reports', 'pdf')
json_dir = os.path.join(parent_dir, 'extract', 'reports', 'json')

# Cria o caminho completo para o diretório trash/pdf
trash_dir = os.path.join(parent_dir, 'extract', 'reports', 'trash', 'pdf')

# Itera sobre todos os arquivos PDF na pasta
for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        # Cria o caminho completo para o arquivo PDF
        file = os.path.join(pdf_dir, filename)

        # Extrai o texto de todas as páginas do arquivo PDF
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)

        lines = []

        for i, page in enumerate(reader.pages):
            print(f"Extraindo texto do arquivo {filename}, página {i+1}/{number_of_pages}...")
            text = page.extract_text()

            # divide o texto em linhas e remove espaços em branco no início e no final de cada linha
            for line in text.splitlines():
                clean_line = line.strip()
                if clean_line:
                    lines.append(clean_line)

        # Cria um dicionário com uma chave "lines" que contém a lista de linhas como valor
        data = {"lines": lines}
        
        # Salva o dicionário como um objeto JSON em um arquivo com o nome do arquivo PDF correspondente
        output_file = os.path.join(json_dir, f"{os.path.splitext(filename)[0]}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        
        # Cria o caminho completo para o arquivo PDF na pasta trash/pdf
        trash_file = os.path.join(trash_dir, filename)

        # Move o arquivo PDF para a pasta trash/pdf
        os.rename(file, trash_file)
