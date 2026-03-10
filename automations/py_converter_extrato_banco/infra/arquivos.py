import pandas as pd


def abrir_arquivo(arquivo, header=None):
    """Open an Excel file and return a DataFrame.

    Pandas chooses an engine by extension. For ``.xls`` files the default
    engine requires the xlrd package; if that library isn't installed we
    re-raise a friendlier message explaining how to fix the environment.
    """
    try:
        df = pd.read_excel(arquivo, header=header)
        return df
    except ImportError as e:
        raise ImportError(
            "Erro ao abrir arquivo Excel: instale 'xlrd>=2.0.1' para permitir "
            "a leitura de arquivos .xls (pandas o usa como engine)."
        ) from e
