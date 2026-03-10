import importlib
import uuid
import time
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from backend.app.utils.logger import create_logger

executions = {}
MAX_CONCURRENT_EXECUTIONS = int(os.getenv("MAX_CONCURRENT_EXECUTIONS", 5))
EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", 300))  # 5 minutos
EXECUTION_MEMORY_CLEANUP = int(os.getenv("EXECUTION_MEMORY_CLEANUP", 300))  # 5 minutos (vs 1 hora antes)

# Pool de threads com limite de workers = MAX_CONCURRENT_EXECUTIONS
executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_EXECUTIONS)


def run_automation_background(nome_automacao):
    """
    Executa a automação no background.
    Agora retorna o resultado em vez de modificar dicionário diretamente.
    """
    try:
        module_path = f"automations.{nome_automacao}.main"
        module = importlib.import_module(module_path)
        
        log_file = create_logger(nome_automacao)
        
        context = {
            "automation_name": nome_automacao,
            "log_file": log_file,
            "data_dir": "data",
            "timeout": EXECUTION_TIMEOUT
        }
        
        result = module.run(context)
        
        return {
            "status": "completed",
            "result": result,
            "log": log_file
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def _cleanup_old_executions():
    """Remove execuções completadas/com erro que passaram de EXECUTION_MEMORY_CLEANUP"""
    current_time = time.time()
    expired = [
        exec_id for exec_id, data in executions.items()
        if data.get("status") in ["completed", "error"]
        and (current_time - data.get("start_time", current_time)) > EXECUTION_MEMORY_CLEANUP
    ]
    for exec_id in expired:
        del executions[exec_id]


def start_automation(nome_automacao):
    """
    Inicia a automação com timeout REAL via ThreadPoolExecutor.
    """
    # Limpeza de execuções antigas
    _cleanup_old_executions()
    
    # Verificar limite de execuções simultâneas
    running_count = sum(1 for exec_data in executions.values() if exec_data["status"] == "running")
    if running_count >= MAX_CONCURRENT_EXECUTIONS:
        raise Exception("Limite de execuções simultâneas atingido")
    
    execution_id = str(uuid.uuid4())
    
    executions[execution_id] = {
        "automation": nome_automacao,
        "status": "running",
        "start_time": time.time()
    }
    
    # Enviar execução para o pool com timeout real
    try:
        future = executor.submit(run_automation_background, nome_automacao)
        
        # Esperar resultado com timeout - se exceder EXECUTION_TIMEOUT, cancela
        result = future.result(timeout=EXECUTION_TIMEOUT)
        
        # Atualizar com resultado
        executions[execution_id].update(result)
        
    except FuturesTimeoutError:
        executions[execution_id]["status"] = "error"
        executions[execution_id]["error"] = f"Timeout: execução excedeu {EXECUTION_TIMEOUT}s"
    except Exception as e:
        executions[execution_id]["status"] = "error"
        executions[execution_id]["error"] = str(e)
    
    return execution_id


def get_execution(execution_id):
    """Obter status da execução e limpar se necessário"""
    _cleanup_old_executions()
    
    exec_data = executions.get(execution_id)
    if not exec_data:
        return {"erro": "execução não encontrada"}
    
    return exec_data
