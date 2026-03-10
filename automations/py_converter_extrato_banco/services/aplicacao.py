from ..infra.caminhos import Caminhos
from .processador_extrato import ProcessadorExtrato
from ..core.nome_arquivo import NomeArquivoExtrato
from ..infra.organizador import OrganizadorArquivos
from ..regras.bancos import extrair_data
from ..infra.arquivos import abrir_arquivo
from ..infra.logger import configurar_logger
from ..core.notificador import Notificador
from pathlib import Path


class AplicacaoExtrato:

    def __init__(self):
        self.caminhos = Caminhos()
        self.processador = ProcessadorExtrato()
        self.nomeador = NomeArquivoExtrato()
        self.organizador = OrganizadorArquivos()
        self.notificador = Notificador()
        self.logger = configurar_logger(self.caminhos.base)

    def registrar_interface(self, funcao_callback):
        self.notificador.registrar_callback(funcao_callback)

    def processar_arquivo(self, caminho_arquivo):

        self.caminhos.garantir_base()

        nome_arquivo = Path(caminho_arquivo).name

        try:

            df_original = abrir_arquivo(caminho_arquivo, header=None)

            df_tratado, banco = self.processador.processar(caminho_arquivo)

            mes, ano = extrair_data(df_original, banco)

            nome_final = self.nomeador.criar_nome(df_original, banco)

            self.caminhos.garantir_saida()
            self.caminhos.garantir_salvar()

            self.organizador.salvar_csv(
                df_tratado,
                nome_final,
                mes,
                ano,
                self.caminhos.saida
            )

            novo_caminho = self.organizador.renomear_arquivo(
                caminho_arquivo,
                nome_final
            )

            novo_caminho = self.organizador.mover_para_subpasta(
                novo_caminho,
                mes,
                ano,
                self.caminhos.salvar
            )

            self.logger.info(f"Processado com sucesso: {nome_arquivo}")

            self.notificador.notificar(
                f"✅ {nome_arquivo} processado com sucesso.",
                "sucesso"
            )

            return True  # sucesso

        except Exception as e:

            self.logger.error(
                f"Erro ao processar {nome_arquivo}: {str(e)}",
                exc_info=True
            )

            self.notificador.notificar(
                f"❌ Erro ao processar {nome_arquivo}:\n{str(e)}",
                "erro"
            )

            self.caminhos.garantir_em_branco()

            self.organizador.mover_para_em_branco(
                caminho_arquivo,
                self.caminhos.em_branco
            )

            return False  # erro