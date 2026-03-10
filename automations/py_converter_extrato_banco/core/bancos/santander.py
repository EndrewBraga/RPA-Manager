import pandas as pd


class SantanderProcessor:

    HEADER_LINHA = 2

    def tratar(self, df_raw):
        df = df_raw.copy()

        df["Documento"] = self._transformar_codigo(df)
        df["Valor"] = self._transformar_valor(df)

        df_tratado = df[["Data", "Documento", "Histórico", "Valor"]].copy()
        df_tratado.columns = ["Data", "Codigo", "Descricao", "Valor"]

        df_tratado = self._excluir_saldo_inicial(df_tratado)

        return df_tratado

    def _transformar_valor(self, df):
        valor = df["Valor (R$)"]

        return pd.to_numeric(valor, errors="coerce")

    def _transformar_codigo(self, df):
        return (
            df["Documento"]
            .astype(str)
            .str.replace(".0", "", regex=False)
        )

    def _excluir_saldo_inicial(self, df):
        indice = df[
            df["Descricao"]
            .astype(str)
            .str.contains("SALDO ANTERIOR", case=False, na=False)
        ].index

        if not indice.empty:
            df = df.drop(indice[0])

        return df