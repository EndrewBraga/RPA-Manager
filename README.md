# RPA-Manager
Sistema de Gerenciamento de Automações

## Descrição
Este projeto é um sistema de RPA (Robotic Process Automation) para gerenciar e executar automações personalizadas. Ele inclui um backend em FastAPI, um frontend simples em HTML/JS e uma estrutura modular para adicionar novas automações.

## Arquitetura
- **Backend**: API REST em FastAPI para listar, executar e monitorar automações.
- **Frontend**: Interface web básica para interação com o backend.
- **Automações**: Scripts Python modulares na pasta `automations/`. Cada automação deve ter um diretório com `main.py` contendo uma função `run(context)` que retorna o resultado.
- **Logs**: Os arquivos de log ficam num diretório global `logs/` no repositório, com uma subpasta para cada automação (por exemplo `logs/py_converter_extrato_banco/processamento.log`). Dessa forma não são escritas em diretórios pessoais nem misturadas com os dados do usuário.

## Instalação
1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv .venv`
3. Ative: `.venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Copie `.env.example` para `.env` e ajuste as configurações.
6. Execute o backend: `uvicorn backend.app.main:app --reload`
7. Abra `frontend/index.html` no navegador.

## Testes
Execute `pytest` para rodar os testes.

## Adicionando Automações
- Crie uma pasta em `automations/` com a estrutura de uma automação (por exemplo, `automations/minha_automacao/`).
- Crie um arquivo `__init__.py` e um arquivo `main.py` dentro da pasta.
- Implemente a função `run(context)` no `main.py` que retorna o resultado.
- Opcionalmente, adicione um `prepare()` que será chamado ao abrir a página da automação.
- A automação será detectada automaticamente e aparecerá na lista.

## Uso
- Acesse o frontend para listar e executar automações.
- O painel possui design profissional com tema escuro inspirado em padrões modernos:
  - Paleta de cores sóbria com acentos verdes para ações
  - Cabeçalho fixo discretamente sombreado
  - Cards de automação em grid responsivo com hover interativo
  - Sistema de feedback visual para status de execução
- Ao abrir a página de uma automação, o ambiente necessário será preparado automaticamente.
- Clique no card da automação para abrir sua página de execução.

## Desenvolvimento
- Adicione testes em `tests/`.
- Use variáveis de ambiente para configuração (ex.: `API_URL`).
- Para produção, restrinja CORS e adicione autenticação.

## Licença
MIT
