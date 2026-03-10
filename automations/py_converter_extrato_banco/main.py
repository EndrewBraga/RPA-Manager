import glob

from .services.aplicacao import AplicacaoExtrato
from .infra.caminhos import Caminhos
from .infra.logger import configurar_logger


class LoggerCallback:
    def __init__(self, base_path):
        self.logger = configurar_logger(base_path)

    def __call__(self, mensagem, tipo="info"):
        if tipo == "erro":
            self.logger.error(mensagem)
        elif tipo == "sucesso":
            self.logger.info(f"SUCCESS: {mensagem}")
        else:
            self.logger.info(mensagem)
        # console printing removed; logs are written to file only (simpler output)



def main():
    # prepare environment and application
    caminhos = Caminhos()
    caminhos.garantir_base()

    callback = LoggerCallback(caminhos.base)
    app = AplicacaoExtrato()
    app.registrar_interface(callback)

    arquivos = glob.glob(str(caminhos.entrada / "*.xls"))
    total_arquivos = len(arquivos)
    processados = 0
    erros = 0

    if not arquivos:
        callback("⚠ Nenhum arquivo encontrado.", "info")
        return {
            "status": "completed",
            "total_arquivos": 0,
            "processados": 0,
            "erros": 0,
            "mensagem": "Nenhum arquivo encontrado para processar."
        }

    for arquivo in arquivos:
        sucesso = app.processar_arquivo(arquivo)
        if sucesso:
            processados += 1
        else:
            erros += 1

    mensagem = f"Processamento concluído: {processados} de {total_arquivos} arquivos processados com sucesso."
    if erros > 0:
        mensagem += f" {erros} erros ocorreram."

    return {
        "status": "completed",
        "total_arquivos": total_arquivos,
        "processados": processados,
        "erros": erros,
        "mensagem": mensagem
    }


def prepare():
    """Create any required directories before the automation runs.

    This was previously done when the GUI opened; we call it at startup or
    when listing automations so that the "Converter Extratos" folder exists
    even before processing begins.
    """
    caminhos = Caminhos()
    caminhos.garantir_base()


def run(context=None):
    """Entry point used by the orchestration layer.

    The simple context dictionary may contain keys like
    ``log_file`` or ``data_dir`` but is currently ignored.
    """
    result = main()
    return result


if __name__ == "__main__":
    main()
