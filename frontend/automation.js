const API_URL = window.location.origin

const urlParams = new URLSearchParams(window.location.search)
const automationName = urlParams.get('name')

const titleDiv = document.getElementById("automation-title")
const descDiv = document.getElementById("automation-description")
const runBtn = document.getElementById("run-btn")
const btnStatusDiv = document.getElementById("btn-status")
const statusSection = document.getElementById("status-section")
const statusIcon = document.getElementById("status-icon")
const statusText = document.getElementById("status-text")
const resultSection = document.getElementById("result-section")
const resultDiv = document.getElementById("result")

const friendlyNames = {
    'py_converter_extrato_banco': 'Converter Extrato',
};

if (!automationName) {
    titleDiv.innerText = "Erro"
    descDiv.innerText = "Automação não especificada"
    runBtn.disabled = true
} else {
    const friendlyName = friendlyNames[automationName] || automationName;
    titleDiv.innerText = friendlyName
    descDiv.innerText = "Clique no botão abaixo para iniciar a execução desta automação"
    prepareAutomation(automationName)
    runBtn.onclick = () => runAutomation(automationName)
}

async function prepareAutomation(name) {
    try {
        const res = await fetch(API_URL + "/prepare/" + name, { method: "POST" })
        if (!res.ok) throw new Error(`Erro na preparação`)
        btnStatusDiv.innerText = "✓ Pronto para executar"
        btnStatusDiv.className = "btn-hint success"
    } catch (error) {
        btnStatusDiv.innerText = "⚠ Erro ao preparar o ambiente"
        btnStatusDiv.className = "btn-hint error"
    }
}

async function runAutomation(name) {
    try {
        runBtn.disabled = true
        runBtn.innerText = "⏳ Executando..."
        
        const res = await fetch(API_URL + "/run/" + name, { method: "POST" })
        if (!res.ok) throw new Error(`Falha ao iniciar`)
        const data = await res.json()
        
        showStatus()
        updateStatusIcon("running")
        statusText.innerText = "Executando automação..."
        resultSection.style.display = "none"
        
        checkStatus(data.execution_id)
    } catch (error) {
        updateStatusIcon("error")
        statusText.innerText = `❌ Erro: ${error.message}`
        showStatus()
        runBtn.disabled = false
        runBtn.innerText = "▶ Tentar Novamente"
    }
}

function updateStatusIcon(status) {
    if (status === "running") {
        statusIcon.innerHTML = '<span class="spinner"></span>'
    } else if (status === "completed") {
        statusIcon.innerHTML = "✅"
        statusIcon.style.color = "var(--color-accent)"
    } else if (status === "error") {
        statusIcon.innerHTML = "❌"
        statusIcon.style.color = "#ff6b6b"
    }
}

function showStatus() {
    statusSection.style.display = "block"
}

function formatResult(result) {
    if (!result) return "<p>Nenhum resultado disponível</p>"
    
    let html = ""
    
    // Status
    if (result.status) {
        const statusEmoji = result.status === "success" ? "✅" : "❌"
        html += `<div class="result-item"><strong>${statusEmoji} Status:</strong> ${result.status}</div>`
    }
    
    // Mensagem
    if (result.mensagem) {
        html += `<div class="result-item"><strong>📝 Mensagem:</strong> ${result.mensagem}</div>`
    }
    
    // Arquivo de saída
    if (result.arquivo_saida) {
        html += `<div class="result-item"><strong>📄 Arquivo:</strong> ${result.arquivo_saida}</div>`
    }
    
    // Estatísticas
    if (result.stats && Object.keys(result.stats).length > 0) {
        html += `<div class="result-item"><strong>📊 Estatísticas:</strong>`
        for (const [key, value] of Object.entries(result.stats)) {
            html += `<br>&nbsp;&nbsp;• ${key}: ${value}`
        }
        html += `</div>`
    }
    
    // Detalhes adicionais
    if (result.detalhes) {
        html += `<div class="result-item"><strong>ℹ️ Detalhes:</strong> ${result.detalhes}</div>`
    }
    
    return html || "<p>Execução concluída.</p>"
}

function checkStatus(id) {
    const interval = setInterval(async () => {
        try {
            const res = await fetch(API_URL + "/execution/" + id)
            if (!res.ok) throw new Error("Erro ao verificar status")
            const data = await res.json()
            
            if (data.status === "completed") {
                updateStatusIcon("completed")
                statusText.innerText = "✅ Execução Concluída com Sucesso!"
                resultSection.style.display = "block"
                resultDiv.innerHTML = formatResult(data.result)
                runBtn.disabled = false
                runBtn.innerText = "▶ Executar Novamente"
                clearInterval(interval)
            } else if (data.status === "error") {
                updateStatusIcon("error")
                statusText.innerText = `❌ Execução Falhou: ${data.error}`
                resultSection.style.display = "block"
                resultDiv.innerText = `Erro: ${data.error}`
                runBtn.disabled = false
                runBtn.innerText = "▶ Tentar Novamente"
                clearInterval(interval)
            }
        } catch (error) {
            updateStatusIcon("error")
            statusText.innerText = `❌ Erro ao verificar: ${error.message}`
            runBtn.disabled = false
            runBtn.innerText = "▶ Tentar Novamente"
            clearInterval(interval)
        }
    }, 2000)
}