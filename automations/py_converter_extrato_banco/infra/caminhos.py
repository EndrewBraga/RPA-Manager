from pathlib import Path
import sys


class Caminhos:

    def __init__(self):
        self._definir_base()
        self._definir_subpastas()

    def _definir_base(self):
        if getattr(sys, "frozen", False):
            base_execucao = Path(sys.executable).parent
        else:
            base_execucao = Path.home() / "Downloads"

        self.base = base_execucao / "Converter Extratos"

    def _definir_subpastas(self):
        self.entrada = self.base
        self.saida = self.base / "Importar"
        self.em_branco = self.base / "Erro"
        self.salvar = self.base / "Salvar"

    def garantir_base(self):
        self.base.mkdir(parents=True, exist_ok=True)

    def garantir_entrada(self):
        self.entrada.mkdir(parents=True, exist_ok=True)

    def garantir_saida(self):
        self.saida.mkdir(parents=True, exist_ok=True)

    def garantir_em_branco(self):
        self.em_branco.mkdir(parents=True, exist_ok=True)

    def garantir_salvar(self):
        self.salvar.mkdir(parents=True, exist_ok=True)