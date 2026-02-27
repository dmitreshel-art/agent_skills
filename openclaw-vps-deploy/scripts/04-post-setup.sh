#!/bin/bash
# OpenClaw VPS Setup - Step 4: Post-Setup Configuration
# Configures sandbox, memory, and local embeddings

set -e

# Arguments
OLLAMA_API_KEY="${OLLAMA_API_KEY:-}"
DEFAULT_MODEL="${DEFAULT_MODEL:-gpt-oss:120b}"

echo "=== Step 4: Post-Setup Configuration ==="

CONFIG_DIR="/home/openclaw/.openclaw"
WORKSPACE="$CONFIG_DIR/workspace"

# Ensure directories exist
mkdir -p "$CONFIG_DIR"
mkdir -p "$WORKSPACE/memory"

# Set ownership
chown -R openclaw:openclaw "$CONFIG_DIR"
chmod -R 755 "$CONFIG_DIR"

# Create openclaw.json with Ollama Cloud + sandbox + local embeddings
echo "Creating OpenClaw configuration..."
cat > "$CONFIG_DIR/openclaw.json" << 'OPENCLAW_CONFIG'
{
  models: {
    providers: {
      ollama: {
        baseUrl: "https://ollama.com",
        apiKey: "${OLLAMA_API_KEY}"
      }
    }
  },
  agents: {
    defaults: {
      model: { primary: "ollama/OPENCLAW_DEFAULT_MODEL" },
      sandbox: {
        mode: "non-main",
        scope: "agent",
        workspaceAccess: "none",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          network: "none",
          user: "1000:1000"
        }
      },
      memorySearch: {
        provider: "local",
        local: {
          modelPath: "hf:keisuke-miyako/multilingual-e5-small-gguf-q8_0/multilingual-e5-small-Q8_0.gguf"
        }
      },
      compaction: {
        mode: "safeguard",
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 6000
        }
      }
    }
  },
  gateway: {
    mode: "local",
    bind: "loopback",
    port: 18789
  }
}
OPENCLAW_CONFIG

# Replace placeholder with actual model
sed -i "s/OPENCLAW_DEFAULT_MODEL/$DEFAULT_MODEL/g" "$CONFIG_DIR/openclaw.json"

# Store API key in .env
if [ -n "$OLLAMA_API_KEY" ]; then
    echo "OLLAMA_API_KEY=$OLLAMA_API_KEY" > "$CONFIG_DIR/.env"
    chmod 600 "$CONFIG_DIR/.env"
fi

# Create MEMORY.md template
echo "Creating MEMORY.md template..."
cat > "$WORKSPACE/MEMORY.md" << 'MEMORY_TEMPLATE'
# Память

## Обо мне
- Имя: [заполнить]
- Часовой пояс: [заполнить]

## Предпочтения
- Язык: русский
- Формат ответов: краткий

## Проекты
- [добавлять проекты по мере работы]

## Важное
- [ключевые факты и решения]
MEMORY_TEMPLATE

# Create today's memory log
TODAY=$(date +%Y-%m-%d)
touch "$WORKSPACE/memory/$TODAY.md"

# Set ownership
chown -R openclaw:openclaw "$CONFIG_DIR"
chown -R openclaw:openclaw "$WORKSPACE"

echo ""
echo "=== Step 4 Complete ==="
echo "Configuration: $CONFIG_DIR/openclaw.json"
echo "Workspace: $WORKSPACE"
echo "Memory: $WORKSPACE/MEMORY.md"
echo "Embeddings: multilingual-e5-small (local, ~120 MB)"
echo ""
echo "✅ Sandbox enabled (non-main sessions)"
echo "✅ Memory configured"
echo "✅ Local embeddings ready"
echo ""
