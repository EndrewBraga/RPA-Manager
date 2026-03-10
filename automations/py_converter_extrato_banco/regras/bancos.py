import pandas as pd


def selecionar_celula_banco(df):
    valor_celula = str(df.iloc[1, 1]).strip()
    return valor_celula


def extrair_data_bradesco(df):
    data = pd.to_datetime(df.iloc[10, 0], dayfirst=True)
    mes = data.month
    ano = data.year
    return mes, ano


def extrair_data_santander(df):
    data = pd.to_datetime(df.iloc[4, 0], dayfirst=True)
    mes = data.month
    ano = data.year
    return mes, ano


def extrair_data(df, banco):
    if banco == "Bradesco":
        mes, ano = extrair_data_bradesco(df)
    elif banco == "Santander":
        mes, ano = extrair_data_santander(df)
    else:
        raise ValueError("Banco desconhecido. Não é possível tratar os dados.")
    return mes, ano