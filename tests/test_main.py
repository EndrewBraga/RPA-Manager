import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_list_automations():
    response = client.get("/automations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_run_invalid_automation():
    response = client.post("/run/invalid_automation")
    assert response.status_code == 404


def test_prepare_invalid_automation():
    response = client.post("/prepare/invalid_automation")
    assert response.status_code == 404


def test_get_invalid_execution():
    response = client.get("/execution/invalid_id")
    assert response.status_code == 404


def test_automation_page_contents():
    response = client.get("/automation")
    assert response.status_code == 200
    html = response.text
    assert 'id="run-btn"' in html
    assert 'id="prepare-btn"' not in html
    assert 'Voltar para lista' not in html
    assert '<a href="/"' in html
    # should have hero header and user-friendly elements
    assert 'class="hero"' in html
    assert 'id="automation-title"' in html
    assert 'id="status-section"' in html
    assert 'class="btn-primary"' in html

def test_index_page_layout():
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    # brand link should exist somewhere in document
    assert 'class="brand"' in html
    assert 'RPA Manager' in html
    assert '<input id="search-input"' in html
    assert 'Automações Disponíveis' in html
    # page itself shouldn't contain the old open button label
    assert 'Abrir' not in html

    # and the client-side script shouldn't create it either
    script_res = client.get('/static/script.js')
    assert script_res.status_code == 200
    assert 'Abrir' not in script_res.text
    # mapping for friendly name deve estar presente
    assert "'py_converter_extrato_banco': 'Converter Extrato'" in script_res.text

def test_prepare_existing_automation():
    # choose first available automation from list and ensure prepare succeeds
    automations = client.get("/automations").json()
    if automations:
        name = automations[0]
        res = client.post(f"/prepare/{name}")
        assert res.status_code == 200
        body = res.json()
        assert body.get("automation") == name


def test_logger_file_location(tmp_path):
    # logger should create a log under the repo-level logs/<automation> directory
    from automations.py_converter_extrato_banco.infra.logger import configurar_logger
    from pathlib import Path

    base = tmp_path / "base"
    logger = configurar_logger(base)
    logger.info("ping")

    # compute expected path using the same algorithm the logger uses
    import automations.py_converter_extrato_banco.infra.logger as logger_module
    repo_root = Path(logger_module.__file__).resolve().parents[3]
    expected = repo_root / "logs" / "py_converter_extrato_banco" / "processamento.log"

    assert expected.exists(), "log file should live under workspace/logs/<automation>"
    # make sure base directory wasn't used at all for logs
    assert not (base / "logs" / "processamento.log").exists()
    assert not (base / "processamento.log").exists()
