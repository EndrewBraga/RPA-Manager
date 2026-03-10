from .contas import CONTAS


class NomeArquivoExtrato:

    def __init__(self):
        self._estrategias = {
            "Bradesco": self._extrair_conta_bradesco,
            "Santander": self._extrair_conta_santander,
        }

    def criar_nome(self, df, banco):
        try:
            conta = self._estrategias[banco](df)

        except KeyError:
            raise ValueError("Banco não suportado.")

        if conta not in CONTAS:
            raise ValueError(
                f"Conta {conta} não cadastrada no sistema."
            )

        return CONTAS[conta]

    def _extrair_conta_bradesco(self, df):
        texto = str(df.iloc[6, 0])
        conta = texto.split("Conta:")[1].strip()
        return conta

    def _extrair_conta_santander(self, df):
        conta = str(df.iloc[0, 3]).strip()

        if len(conta) > 1:
            conta = conta[:-1] + "-" + conta[-1]

        return conta