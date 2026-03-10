const API_URL = window.location.origin

const automationsDiv = document.getElementById("automations")

// mapa de rótulos amigáveis exibidos nos cards
const friendlyNames = {
    // nome do diretório / automação : texto mostrados
    'py_converter_extrato_banco': 'Converter Extrato',
    // você pode adicionar outras traduções aqui
};

async function loadAutomations(filter="") {
    try {
        const res = await fetch(API_URL + "/automations")
        if (!res.ok) throw new Error(`Erro HTTP: ${res.status}`)
        const automations = await res.json()
        
        // main grid
        automationsDiv.innerHTML = ""
        automations
            .filter(name => name.toLowerCase().includes(filter.toLowerCase()))
            .forEach(name => {
                // make entire card an anchor so clicking anywhere navigates
                const item = document.createElement("a")
                item.className = "automation-item"
                item.href = `/automation?name=${encodeURIComponent(name)}`

                const nameLink = document.createElement("span")
                // keep styling consistent but remove extra link semantics
                nameLink.className = "automation-name"
                // use friendly name if available
                nameLink.innerText = friendlyNames[name] || name

                item.appendChild(nameLink)
                automationsDiv.appendChild(item)
            })
        
    } catch (error) {
        automationsDiv.innerHTML = `<div class="error">Erro ao carregar automações: ${error.message}</div>`
    }
}

// filter as user types
const searchInput = document.getElementById("search-input")
if (searchInput) {
    searchInput.addEventListener("input", (e) => {
        loadAutomations(e.target.value);
    });
}

loadAutomations();