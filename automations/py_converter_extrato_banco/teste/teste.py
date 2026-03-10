import os

from ..infra.arquivos import abrir_arquivo
from ..infra.caminhos import Caminhos

import pandas as pd

def extrair_data_santander(df):
    data = pd.to_datetime(df.iloc[3, 0], dayfirst=True)
    mes = data.month
    ano = data.year
    return mes, ano


if __name__ == "__main__":
    caminhos = Caminhos()
    caminhos.garantir_base()

    arquivo_b = os.path.join(r"C:\Users\endre\Downloads\Converter Extratos", 'Santander Ag. 1679 - CC. 13002792-5 - Construindo Novas Histórias (Dpto 2047).xls')

    df_b = abrir_arquivo(arquivo_b, header=None)

    print(df_b.head(30))

    # mes, ano = extrair_data_santander(df_b)
    # print(f"{mes} e {ano}")
    









# from PIL import Image

# # Caminho da imagem original (PNG ou JPG)
# imagem_original = r"C:\Users\endre\Documents\Programacao\PY_Tratar_importar_reconciliacao\teste\icone.jpg"

# # Nome do arquivo .ico que será criado
# icone_saida = r"C:\Users\endre\Documents\Programacao\PY_Tratar_importar_reconciliacao\teste\icone.ico"

# # Abre a imagem
# img = Image.open(imagem_original)

# # Converte para formato ICO
# img.save(icone_saida, format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])

# print("Ícone criado com sucesso!")