class TransformadorExtrato:

    COLUNAS_PADRAO = ["Data", "Codigo", "Descricao", "Valor"]

    def criar_dataframe(self, df, col_data, col_codigo, col_descricao, col_valor):

        colunas_origem = [col_data, col_codigo, col_descricao, col_valor]

        self._validar_colunas(df, colunas_origem)

        df_tratado = df[colunas_origem].copy()
        df_tratado.columns = self.COLUNAS_PADRAO

        return df_tratado

    def _validar_colunas(self, df, colunas):
        for coluna in colunas:
            if coluna not in df.columns:
                raise ValueError(f"Coluna '{coluna}' não encontrada no arquivo.")