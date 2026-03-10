import pandas as pd


class BradescoProcessor:

    HEADER_LINHA = 8

    def tratar(self, df_raw):
        df = df_raw.copy()

        df = self._cortar_no_total(df)
        df["Valor"] = self._juntar_valores(df)

        df_tratado = df[["Data", "Dcto.", "Lançamento", "Valor"]].copy()
        df_tratado.columns = ["Data", "Codigo", "Descricao", "Valor"]

        df_tratado = self._excluir_saldo_inicial(df_tratado)

        return df_tratado

    def _juntar_valores(self, df):
        valor = df["Crédito (R$)"].combine_first(df["Débito (R$)"])

        return pd.to_numeric(valor, errors="coerce")

    def _cortar_no_total(self, df):
        indice_total = df[
            df["Data"]
            .astype(str)
            .str.contains("total", case=False, na=False)
        ].index

        if not indice_total.empty:
            df = df.loc[:indice_total[0] - 1]

        return df

    def _excluir_saldo_inicial(self, df):
        indice = df[
            df["Descricao"]
            .astype(str)
            .str.contains("SALDO ANTERIOR", case=False, na=False)
        ].index

        if not indice.empty:
            df = df.drop(indice[0])

        return df