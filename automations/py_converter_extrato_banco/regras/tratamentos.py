
def formatar_valores_brasileiro(df, colunas=None):
    """Formata colunas numéricas para o padrão brasileiro (apenas vírgula como decimal)."""
    import pandas as pd
    df_formatado = df.copy()
    if colunas is None:
        colunas = df_formatado.select_dtypes(include=[float, int]).columns
    for col in colunas:
        df_formatado[col] = df_formatado[col].apply(lambda x: f'{x:.2f}'.replace('.', ',') if pd.notnull(x) else x)
    return df_formatado


def excluir_saldo_inicial(df):
    indice_saldo = df[df["Descricao"].astype(str).str.contains("SALDO ANTERIOR", case=False, na=False)].index
    if not indice_saldo.empty:
        df = df.drop(indice_saldo[0])
    return df