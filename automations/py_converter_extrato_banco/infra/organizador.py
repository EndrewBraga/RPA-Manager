from pathlib import Path
import shutil
from ..regras.tratamentos import formatar_valores_brasileiro


class OrganizadorArquivos:

    def salvar_csv(self, df_tratado, nome_arquivo, mes, ano, pasta_saida):
        pasta_saida = Path(pasta_saida)
        pasta_mes = pasta_saida / f"{int(mes):02d}-{ano}"
        pasta_mes.mkdir(parents=True, exist_ok=True)

        if not nome_arquivo.endswith(".csv"):
            nome_arquivo += ".csv"

        caminho_csv = pasta_mes / nome_arquivo

        df_formatado = formatar_valores_brasileiro(df_tratado)

        df_formatado.to_csv(
            caminho_csv,
            index=False,
            sep=";",
            encoding="ISO-8859-1",
        )

        return caminho_csv


    def renomear_arquivo(self, caminho_arquivo, novo_nome):
        caminho_arquivo = Path(caminho_arquivo)

        novo_caminho = caminho_arquivo.with_name(
            f"{novo_nome}{caminho_arquivo.suffix}"
        )

        caminho_arquivo.rename(novo_caminho)

        pdf_original = caminho_arquivo.with_suffix(".pdf")
        if pdf_original.exists():
            novo_pdf = novo_caminho.with_suffix(".pdf")
            pdf_original.rename(novo_pdf)

        return novo_caminho


    def mover_para_subpasta(self, caminho_arquivo, mes, ano, pasta_destino_base):
        caminho_arquivo = Path(caminho_arquivo)

        pasta_destino = Path(pasta_destino_base) / f"{int(mes):02d}-{ano}"
        pasta_destino.mkdir(parents=True, exist_ok=True)

        novo_caminho = pasta_destino / caminho_arquivo.name
        shutil.move(str(caminho_arquivo), str(novo_caminho))

        pdf_original = caminho_arquivo.with_suffix(".pdf")
        if pdf_original.exists():
            destino_pdf = pasta_destino / pdf_original.name
            shutil.move(str(pdf_original), str(destino_pdf))

        return novo_caminho


    def copiar_para_salvar(self, caminho_arquivo, mes, ano, pasta_salvar):
        caminho_arquivo = Path(caminho_arquivo)

        pasta_mes = Path(pasta_salvar) / f"{int(mes):02d}-{ano}"
        pasta_mes.mkdir(parents=True, exist_ok=True)

        destino = pasta_mes / caminho_arquivo.name
        shutil.copy2(str(caminho_arquivo), str(destino))

        pdf_original = caminho_arquivo.with_suffix(".pdf")
        if pdf_original.exists():
            destino_pdf = pasta_mes / pdf_original.name
            shutil.copy2(str(pdf_original), str(destino_pdf))


    def mover_para_em_branco(self, caminho_arquivo, caminho_em_branco: Path):
        caminho_arquivo = Path(caminho_arquivo)

        novo_caminho = caminho_em_branco / caminho_arquivo.name
        shutil.move(str(caminho_arquivo), str(novo_caminho))

        pdf_original = caminho_arquivo.with_suffix(".pdf")
        if pdf_original.exists():
            destino_pdf = caminho_em_branco / pdf_original.name
            shutil.move(str(pdf_original), str(destino_pdf))

        return novo_caminho