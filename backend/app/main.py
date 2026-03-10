# python -m venv .venv
# .venv\Scripts\activate
# pip freeze > requirements.txt
# pip install -r requirements.txt
# uvicorn backend.app.main:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

from backend.app.services.automation_runner import start_automation, get_execution
from backend.app.services.automation_registry import list_automations

load_dotenv()

app = FastAPI(title="RPA Manager", description="API para gerenciamento de automações RPA", version="1.0.0")


# CORS mais seguro: permitir apenas origens específicas
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Servir arquivos estáticos do frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    """
    Serve o frontend principal.
    """
    return FileResponse("frontend/index.html")


@app.get("/automation")
def automation_page():
    """
    Serve a página de automação específica.
    """
    return FileResponse("frontend/automation.html")


@app.get("/automations")
def automations():
    """
    Lista todas as automações disponíveis.
    """
    try:
        return list_automations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar automações: {str(e)}")


@app.post("/run/{nome_automacao}")
def run(nome_automacao: str):
    """
    Inicia a execução de uma automação.
    """
    if not nome_automacao:
        raise HTTPException(status_code=400, detail="Nome da automação é obrigatório")
    
    automations_list = list_automations()
    if nome_automacao not in automations_list:
        raise HTTPException(status_code=404, detail=f"Automação '{nome_automacao}' não encontrada")
    
    try:
        execution_id = start_automation(nome_automacao)
        return {
            "status": "started",
            "execution_id": execution_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar automação: {str(e)}")


@app.post("/prepare/{nome_automacao}")
def prepare_automation(nome_automacao: str):
    """
    Prepara o ambiente para uma automação específica (ex.: cria pastas).
    """
    automations_list = list_automations()
    if nome_automacao not in automations_list:
        raise HTTPException(status_code=404, detail=f"Automação '{nome_automacao}' não encontrada")
    
    try:
        module_path = f"automations.{nome_automacao}.main"
        module = __import__(module_path, fromlist=["*"])
        if hasattr(module, "prepare"):
            module.prepare()
            return {"status": "prepared", "automation": nome_automacao}
        else:
            return {"status": "no_prepare_needed", "automation": nome_automacao}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao preparar automação: {str(e)}")


@app.get("/execution/{execution_id}")
def execution(execution_id: str):
    """
    Consulta o status de uma execução.
    """
    if not execution_id:
        raise HTTPException(status_code=400, detail="ID da execução é obrigatório")
    
    try:
        result = get_execution(execution_id)
        if "erro" in result:
            raise HTTPException(status_code=404, detail=result["erro"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar execução: {str(e)}")