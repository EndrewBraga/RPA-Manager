class Notificador:

    def __init__(self):
        self._callback = None

    def registrar_callback(self, funcao):
        self._callback = funcao

    def notificar(self, mensagem, tipo="info"):
        if self._callback:
            self._callback(mensagem, tipo)