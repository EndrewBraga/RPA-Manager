from ..infra.arquivos import abrir_arquivo
from ..core.detector_banco import DetectorBanco
from ..core.bancos.bradesco import BradescoProcessor
from ..core.bancos.santander import SantanderProcessor


class ProcessadorExtrato:

    PROCESSADORES = {
        "Bradesco": BradescoProcessor,
        "Santander": SantanderProcessor,
    }

    def __init__(self):
        self.detector = DetectorBanco()

    def processar(self, caminho_arquivo):

        df_teste = abrir_arquivo(caminho_arquivo, header=None)

        if df_teste.empty:
            raise ValueError("O arquivo está vazio.")

        if df_teste.shape[1] < 4:
            raise ValueError(
                "O arquivo não possui a estrutura esperada de um extrato."
            )

        banco = self.detector.identificar(df_teste)

        if banco not in self.PROCESSADORES:
            raise ValueError(
                "Banco não suportado ou formato de extrato inválido."
            )

        processor_class = self.PROCESSADORES[banco]
        processor = processor_class()

        df_raw = abrir_arquivo(
            caminho_arquivo,
            header=processor.HEADER_LINHA
        )

        if df_raw.empty:
            raise ValueError(
                "O arquivo não contém dados após o cabeçalho."
            )

        try:
            df_tratado = processor.tratar(df_raw)
        except Exception as e:
            raise ValueError(
                f"Erro ao tratar dados do extrato: {str(e)}"
            )

        return df_tratado, banco