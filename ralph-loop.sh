#!/usr/bin/env bash
# Ralph Loop for Chatvolt MCP
# Runs an autonomous development loop using opencode
#
# Usage:
#   ./ralph-loop.sh              # Run until all checks pass
#   ./ralph-loop.sh -n 5         # Run exactly 5 iterations
#   ./ralph-loop.sh --dry-run    # Show what would happen without running

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RALPH_DIR="$SCRIPT_DIR/ralph"
RALPH_FILE="$RALPH_DIR/RALPH.md"
GUARDRAILS_FILE="$RALPH_DIR/.ralph/guardrails.md"
MAX_ITERATIONS=""
DRY_RUN=false
AGENT_CMD="opencode run --print"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -n, --iterations N    Run exactly N iterations"
    echo "  --agent CMD           Override agent command (default: opencode run --print)"
    echo "  --dry-run             Show assembled prompt without running agent"
    echo "  -h, --help            Show this help message"
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --agent)
            AGENT_CMD="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate ralph file exists
if [[ ! -f "$RALPH_FILE" ]]; then
    echo -e "${RED}Error: $RALPH_FILE not found${NC}"
    exit 1
fi

# Extract frontmatter and body
extract_frontmatter() {
    sed -n '/^---$/,/^---$/p' "$RALPH_FILE" | sed '1d;$d'
}

extract_body() {
    awk '/^---$/{found++; next} found==2{print}' "$RALPH_FILE"
}

# Run a command and capture output
run_command() {
    local cmd="$1"
    local name="$2"
    echo -e "${BLUE}Running: ${name}${NC}"
    eval "$cmd" 2>&1 || true
}

# Resolve placeholders in the prompt
resolve_placeholders() {
    local prompt="$1"
    shift

    # Replace {{ commands.* }} placeholders
    local i=0
    while [[ $i -lt ${#CMD_NAMES[@]} ]]; do
        local name="${CMD_NAMES[$i]}"
        local output="${CMD_OUTPUTS[$i]}"
        prompt="${prompt//\{\{ commands.${name} \}\}/$output}"
        prompt="${prompt//\{\{commands.${name}\}\}/$output}"
        ((i++))
    done

    # Replace {{ ralph.* }} placeholders
    prompt="${prompt//\{\{ ralph.iteration \}\}/$ITERATION}"
    prompt="${prompt//\{\{ralph.iteration\}\}/$ITERATION}"
    prompt="${prompt//\{\{ ralph.max_iterations \}\}/$MAX_ITERATIONS}"
    prompt="${prompt//\{\{ralph.max_iterations\}\}/$MAX_ITERATIONS}"
    prompt="${prompt//\{\{ ralph.name \}\}/chatvolt-mcp}"
    prompt="${prompt//\{\{ralph.name\}\}/chatvolt-mcp}"

    # Replace {{ ralph.guardrails }}
    if [[ -f "$GUARDRAILS_FILE" ]]; then
        local guardrails
        guardrails=$(cat "$GUARDRAILS_FILE")
        prompt="${prompt//\{\{ ralph.guardrails \}\}/$guardrails}"
        prompt="${prompt//\{\{ralph.guardrails\}\}/$guardrails}"
    fi

    # Remove HTML comments
    prompt=$(echo "$prompt" | sed 's/<!--.*-->//g')

    echo "$prompt"
}

# Parse commands from frontmatter
parse_commands() {
    local frontmatter="$1"
    CMD_NAMES=()
    CMD_RUNS=()
    CMD_TIMEOUTS=()

    local in_commands=false
    local current_name=""
    local current_run=""
    local current_timeout="60"

    while IFS= read -r line; do
        if [[ "$line" =~ ^commands: ]]; then
            in_commands=true
            continue
        fi

        if $in_commands; then
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*name:[[:space:]]*(.*) ]]; then
                # Save previous command if exists
                if [[ -n "$current_name" && -n "$current_run" ]]; then
                    CMD_NAMES+=("$current_name")
                    CMD_RUNS+=("$current_run")
                    CMD_TIMEOUTS+=("$current_timeout")
                fi
                current_name="${BASH_REMATCH[1]}"
                current_run=""
                current_timeout="60"
            elif [[ "$line" =~ ^[[:space:]]*run:[[:space:]]*(.*) ]]; then
                current_run="${BASH_REMATCH[1]}"
            elif [[ "$line" =~ ^[[:space:]]*timeout:[[:space:]]*(.*) ]]; then
                current_timeout="${BASH_REMATCH[1]}"
            elif [[ ! "$line" =~ ^[[:space:]] && -n "$line" ]]; then
                in_commands=false
            fi
        fi
    done <<< "$frontmatter"

    # Save last command
    if [[ -n "$current_name" && -n "$current_run" ]]; then
        CMD_NAMES+=("$current_name")
        CMD_RUNS+=("$current_run")
        CMD_TIMEOUTS+=("$current_timeout")
    fi
}

# Main loop
ITERATION=0

echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Chatvolt MCP - Ralph Loop              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Agent: ${AGENT_CMD}${NC}"
if [[ -n "$MAX_ITERATIONS" ]]; then
    echo -e "${BLUE}Max iterations: ${MAX_ITERATIONS}${NC}"
else
    echo -e "${BLUE}Max iterations: unlimited (Ctrl+C to stop)${NC}"
fi
echo ""

# Parse frontmatter
frontmatter=$(extract_frontmatter)
parse_commands "$frontmatter"

echo -e "${BLUE}Commands: ${CMD_NAMES[*]}${NC}"
echo ""

while true; do
    ((ITERATION++))

    if [[ -n "$MAX_ITERATIONS" && $ITERATION -gt $MAX_ITERATIONS ]]; then
        echo -e "${GREEN}✓ Reached max iterations ($MAX_ITERATIONS)${NC}"
        break
    fi

    echo -e "${YELLOW}═══════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  Iteration $ITERATION${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════${NC}"

    # Run all commands
    CMD_OUTPUTS=()
    for i in "${!CMD_NAMES[@]}"; do
        output=$(run_command "${CMD_RUNS[$i]}" "${CMD_NAMES[$i]}")
        CMD_OUTPUTS+=("$output")
    done

    # Extract body and resolve placeholders
    body=$(extract_body)
    prompt=$(resolve_placeholders "$body")

    if $DRY_RUN; then
        echo -e "${BLUE}--- Assembled Prompt ---${NC}"
        echo "$prompt"
        echo -e "${BLUE}--- End Prompt ---${NC}"
        break
    fi

    # Write prompt to temp file
    tmp_prompt=$(mktemp)
    echo "$prompt" > "$tmp_prompt"

    # Run agent
    echo -e "${BLUE}Running agent...${NC}"
    if eval "$AGENT_CMD" < "$tmp_prompt"; then
        echo -e "${GREEN}✓ Agent completed successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Agent exited with non-zero status${NC}"
    fi

    rm -f "$tmp_prompt"

    # Check if all checks pass
    test_output="${CMD_OUTPUTS[0]}"
    lint_output="${CMD_OUTPUTS[1]}"
    format_output="${CMD_OUTPUTS[2]}"

    tests_pass=true
    lint_pass=true
    format_pass=true

    if echo "$test_output" | grep -q "FAILED\|ERROR"; then
        tests_pass=false
    fi

    if echo "$lint_output" | grep -q "Found [0-9]* error"; then
        lint_pass=false
    fi

    if echo "$format_output" | grep -q "Would reformat"; then
        format_pass=false
    fi

    if $tests_pass && $lint_pass && $format_pass; then
        echo ""
        echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
        echo -e "${GREEN}║   All checks passed! Loop complete.      ║${NC}"
        echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
        break
    fi

    echo ""
    if ! $tests_pass; then
        echo -e "${RED}✗ Tests failing${NC}"
    fi
    if ! $lint_pass; then
        echo -e "${RED}✗ Lint errors${NC}"
    fi
    if ! $format_pass; then
        echo -e "${RED}✗ Format issues${NC}"
    fi
    echo ""
done

echo ""
echo -e "${BLUE}Total iterations: $ITERATION${NC}"
