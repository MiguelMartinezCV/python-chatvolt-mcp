#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Chatvolt MCP – Interactive installer
# ---------------------------------------------------------------------------

BOLD="\033[1m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# 1. Check / install uv
# ---------------------------------------------------------------------------
echo -e "\n${BOLD}=== Chatvolt MCP – Instalação ===${RESET}\n"

if ! command -v uv &>/dev/null; then
    info "O gerenciador de pacotes 'uv' não foi encontrado. Instalando..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Make uv available in this session
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v uv &>/dev/null; then
        error "Falha ao instalar o 'uv'. Instale manualmente: https://docs.astral.sh/uv/"
    fi
    success "'uv' instalado com sucesso."
else
    success "'uv' já está instalado: $(uv --version)"
fi

# ---------------------------------------------------------------------------
# 2. Create virtual environment and install dependencies
# ---------------------------------------------------------------------------
info "Criando ambiente virtual e instalando dependências..."
uv venv --quiet
uv sync --quiet
success "Dependências instaladas."

# ---------------------------------------------------------------------------
# 3. Collect CHATVOLT_API_KEY
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}Para obter sua API Key do Chatvolt:${RESET}"
echo -e "  1. Acesse: ${CYAN}https://app.chatvolt.ai/pt-BR/settings/api-keys${RESET}"
echo -e "  2. Crie ou copie uma chave de API existente."
echo ""

# Try to open the URL in the default browser (best-effort)
if command -v xdg-open &>/dev/null; then
    xdg-open "https://app.chatvolt.ai/pt-BR/settings/api-keys" &>/dev/null &
elif command -v open &>/dev/null; then
    open "https://app.chatvolt.ai/pt-BR/settings/api-keys" &>/dev/null &
fi

while true; do
    read -rsp "  Cole sua CHATVOLT_API_KEY aqui e pressione Enter: " CHATVOLT_API_KEY
    echo ""
    if [[ -n "${CHATVOLT_API_KEY}" ]]; then
        break
    fi
    warn "A chave não pode ser vazia. Tente novamente."
done

# ---------------------------------------------------------------------------
# 4. Collect optional HOST / PORT
# ---------------------------------------------------------------------------
echo ""
read -rp "  Host do servidor [padrão: 0.0.0.0]: " SERVER_HOST
SERVER_HOST="${SERVER_HOST:-0.0.0.0}"

read -rp "  Porta do servidor [padrão: 8000]: " SERVER_PORT
SERVER_PORT="${SERVER_PORT:-8000}"

# ---------------------------------------------------------------------------
# 5. Write .env file
# ---------------------------------------------------------------------------
ENV_FILE="$(dirname "$0")/.env"
cat > "${ENV_FILE}" <<EOF
CHATVOLT_API_KEY=${CHATVOLT_API_KEY}
CHATVOLT_BASE_URL=https://api.chatvolt.ai
EOF
success "Arquivo .env criado em ${ENV_FILE}"

# ---------------------------------------------------------------------------
# 6. Update run.py port/host if the user chose non-defaults
# ---------------------------------------------------------------------------
# We pass host and port as environment variables so run.py can pick them up
# without modifying the source file.

# ---------------------------------------------------------------------------
# 7. Start the server
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}Iniciando o servidor Chatvolt MCP...${RESET}"
echo -e "  Endereço: ${GREEN}http://${SERVER_HOST}:${SERVER_PORT}${RESET}"
echo -e "  SSE endpoint: ${GREEN}http://${SERVER_HOST}:${SERVER_PORT}/sse${RESET}"
echo ""
echo -e "  Configure seu cliente MCP com a URL:"
echo -e "  ${CYAN}http://localhost:${SERVER_PORT}${RESET}"
echo ""
echo -e "  Pressione ${BOLD}Ctrl+C${RESET} para parar o servidor."
echo ""

MCP_HOST="${SERVER_HOST}" MCP_PORT="${SERVER_PORT}" \
    uv run python -c "
import uvicorn, os, sys
sys.path.append('.')
host = os.environ.get('MCP_HOST', '0.0.0.0')
port = int(os.environ.get('MCP_PORT', 8000))
uvicorn.run('src.server:starlette_app', host=host, port=port, log_level='info')
"
