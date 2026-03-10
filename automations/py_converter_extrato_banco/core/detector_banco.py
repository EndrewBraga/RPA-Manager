import pandas as pd


class DetectorBanco:

    REGRAS = {
        "Bradesco": lambda v: v == "Bradesco Net Empresa",
        "Santander": lambda v: pd.isna(v),
    }

    def identificar(self, df):

        valor = self._obter_valor_referencia(df)

        for banco, regra in self.REGRAS.items():
            if regra(valor):
                return banco

        return "Desconhecido"

    def _obter_valor_referencia(self, df):
        try:
            return df.iloc[1, 1]
        except Exception:
            return None