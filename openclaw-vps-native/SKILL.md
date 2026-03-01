---
name: openclaw-vps-native
description: Deploy OpenClaw on Ubuntu VPS with native Node.js installation (no Docker). Use when the user wants to deploy OpenClaw without containers, prefers direct installation, or has resource constraints. Includes security hardening, systemd daemon, and optional HTTPS/Telegram. Based on official docs.openclaw.ai guides.
---

# OpenClaw VPS Native (Без Docker)

Развёртывание OpenClaw на Ubuntu VPS через нативную установку Node.js. Без контейнеров, меньше overhead. Основано на официальной документации OpenClaw.

## Ссылки на официальную документацию

- **Установка:** https://docs.openclaw.ai/install/
- **Node.js:** https://docs.openclaw.ai/install/node
- **Hetzner (Docker):** https://docs.openclaw.ai/install/hetzner (для сравнения)
- **Gateway:** https://docs.openclaw.ai/gateway/
- **Remote Access:** https://docs.openclaw.ai/gateway/remote
- **Security:** https://docs.openclaw.ai/gateway/security

## Архитектура

```
VPS (Ubuntu 22.04+)
├── UFW Firewall (22, 80, 443 only)
├── Node.js 22.x (native)
├── OpenClaw (npm global: npm install -g openclaw@latest)
├── Systemd daemon (openclaw gateway via --install-daemon)
├── Nginx (reverse proxy) → https://domain.com
│   └── HTTP + WebSocket → OpenClaw :18789
└── OpenClaw Gateway
    ├── Gateway :18789 (HTTP + WebSocket)
    └── Channels (Telegram, etc.)
        ↑
Данные: ~/.openclaw/ (HOME пользователя)
├── openclaw.json (конфиг)
├── .openclaw.env (секреты, права 600)
└── workspace/
    ├── MEMORY.md
    └── memory/
```

## Преимущества vs Docker

| Аспект | Native | Docker |
|--------|--------|--------|
| Память | Меньше (нет overlay) | Больше |
| Запуск | Прямой systemd | docker compose |
| Обновление | `npm update -g openclaw` | Пересборка образа |
| Изоляция | Нет | Да |
| Отладка | `journalctl -u openclaw-gateway` | `docker compose logs` |
| Бинарники | Устанавливаются в систему | Нужно печь в Dockerfile |

---

## Workflow

### Шаг 1: Сбор данных

Спроси последовательно:
1. IP адрес VPS?
2. SSH пользователь и пароль/ключ?
3. Model provider? (Anthropic API key / OpenAI / Ollama Cloud / Custom)
4. Домен для HTTPS? (опционально, но рекомендуется для Control UI)
5. Telegram bot token? (опционально)
6. Нужен ли remote access через SSH tunnel или Tailscale?

### Шаг 2: Подготовка VPS

```bash
# SSH подключение
ssh user@IP

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Создание пользователя openclaw (опционально, можно использовать существующего)
sudo useradd -m -s /bin/bash openclaw
sudo usermod -aG sudo openclaw

# SSH ключ для openclaw (если создаёшь нового пользователя)
sudo mkdir -p /home/openclaw/.ssh
sudo cp ~/.ssh/authorized_keys /home/openclaw/.ssh/
sudo chown -R openclaw:openclaw /home/openclaw/.ssh
sudo chmod 700 /home/openclaw/.ssh
sudo chmod 600 /home/openclaw/.ssh/authorized_keys
```

### Шаг 3: UFW Firewall

**Критически важно!** Настрой файрвол ДО запуска сервисов.

```bash
# Установка и настройка UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Проверка
sudo ufw status
# Должно быть: 22, 80, 443 разрешены, остальное закрыто
```

⚠️ **НЕ открывай порт 18789 публично!** Gateway — loopback или lan только.

**Security model (из официальной документации):**
- `loopback` (127.0.0.1) — безопасно по умолчанию, доступ через SSH tunnel
- `lan` (0.0.0.0) — для VPS с Nginx reverse proxy + auth token
- `tailnet` — для Tailscale сетей

### Шаг 4: Node.js установка

```bash
# Установка Node.js 22.x (требуется 22+)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Проверка
node -v  # v22.x.x или выше
npm -v   # 10.x.x

# Установка build tools (для нативных модулей типа sharp)
sudo apt install -y build-essential python3
```

**Альтернатива: версия через version manager (fnm, nvm):**
```bash
# fnm (рекомендуется)
fnm install 22
fnm use 22

# Не забудь добавить в ~/.bashrc или ~/.zshrc!
```

### Шаг 5: Установка OpenClaw

#### Рекомендуемый метод: Installer script

```bash
# Быстрая установка с onboarding
curl -fsSL https://openclaw.ai/install.sh | bash

# Или без onboarding (для скриптов)
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

#### Альтернатива: npm global

```bash
# Установка OpenClaw глобально
npm install -g openclaw@latest

# Проверка
openclaw --version

# Если команда не найдена — добавь в PATH
export PATH="$(npm prefix -g)/bin:$PATH"
# Добавь в ~/.bashrc для постоянства
```

**Если sharp fails (libvips):**
```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

### Шаг 6: Onboarding / Конфигурация

**Интерактивный режим (для ручной установки):**
```bash
openclaw onboard --install-daemon
```

**Полностью автоматический режим (для скриптов/VPS):**

```bash
# Генерация токена Gateway
GATEWAY_TOKEN=$(openssl rand -hex 32)

# Non-interactive onboarding
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --mode local \
  --flow quickstart \
  --workspace ~/.openclaw/workspace \
  --gateway-bind lan \
  --gateway-port 18789 \
  --gateway-auth token \
  --gateway-token "$GATEWAY_TOKEN" \
  --auth-choice anthropic-api-key \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --install-daemon \
  --skip-channels \
  --skip-skills \
  --skip-ui
```

**Параметры для --non-interactive:**

| Параметр | Описание |
|----------|----------|
| `--non-interactive` | Без промптов |
| `--accept-risk` | Подтверждение рисков (обязательно) |
| `--mode local` | Локальный gateway (vs remote) |
| `--flow quickstart` | Быстрая настройка (vs advanced) |
| `--gateway-bind lan` | Bind на 0.0.0.0 (для VPS/Nginx) |
| `--gateway-port 18789` | Порт |
| `--gateway-auth token` | Auth через токен |
| `--gateway-token` | Токен (или сгенерировать) |
| `--auth-choice` | Провайдер: anthropic-api-key, openai-api-key, custom-api-key, etc. |
| `--install-daemon` | Установить systemd сервис |
| `--skip-channels` | Пропустить настройку каналов |
| `--skip-skills` | Пропустить установку skills |
| `--skip-ui` | Пропустить UI промпты |

**Провайдеры API ключей (--auth-choice):**
- `anthropic-api-key` — Anthropic Claude
- `openai-api-key` — OpenAI
- `gemini-api-key` — Google Gemini
- `zai-api-key` — Z.AI
- `openrouter-api-key` — OpenRouter
- `custom-api-key` — Custom provider (нужен `--custom-base-url`)
- `skip` — пропустить, настроить позже

**Custom provider (Ollama Cloud, локальный Ollama, etc.):**
```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --mode local \
  --flow quickstart \
  --gateway-bind lan \
  --gateway-port 18789 \
  --auth-choice custom-api-key \
  --custom-provider-id ollama \
  --custom-base-url "https://ollama.com/v1" \
  --custom-compatibility openai \
  --custom-model-id "glm-5" \
  --install-daemon \
  --skip-channels \
  --skip-skills
```

**Без API ключа (настроить позже):**
```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --mode local \
  --flow quickstart \
  --gateway-bind lan \
  --gateway-port 18789 \
  --auth-choice skip \
  --install-daemon \
  --skip-channels \
  --skip-skills \
  --skip-ui
```

**Что делает onboard:**
1. Model/Auth — настройка провайдера (Anthropic, OpenAI, Custom)
2. Workspace — расположение файлов (по умолчанию ~/.openclaw/workspace)
3. Gateway — порт, bind, auth mode
4. Channels — WhatsApp, Telegram, Discord, etc. (можно пропустить)
5. Daemon — установка systemd user unit
6. Health check — проверка запуска (можно пропустить)

---

## Полный скрипт автоматической установки

Для развёртывания на VPS без интерактивного ввода:

```bash
#!/bin/bash
# openclaw-vps-install.sh — автоматическая установка OpenClaw на VPS
# Usage: ./openclaw-vps-install.sh

set -e

# === КОНФИГУРАЦИЯ (переопредели через env vars) ===
OPENCLAW_GATEWAY_BIND="${OPENCLAW_GATEWAY_BIND:-lan}"
OPENCLAW_GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
OPENCLAW_WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"

# API ключи (обязательные или пусто для skip)
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"
OPENAI_API_KEY="${OPENAI_API_KEY:-}"
OLLAMA_API_KEY="${OLLAMA_API_KEY:-}"

# Custom provider (если используешь)
CUSTOM_PROVIDER_ID="${CUSTOM_PROVIDER_ID:-}"
CUSTOM_BASE_URL="${CUSTOM_BASE_URL:-}"
CUSTOM_MODEL_ID="${CUSTOM_MODEL_ID:-}"

# Ollama Cloud модели (через запятую, обязательно если OLLAMA_API_KEY)
OLLAMA_MODELS="${OLLAMA_MODELS:-}"

# Telegram (опционально)
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"

# === ПРОВЕРКИ ===
echo "✓ Проверка Node.js..."
if ! command -v node &> /dev/null; then
    echo "Node.js не установлен. Установка..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo "❌ Требуется Node.js 22+. Установлено: $(node -v)"
    exit 1
fi
echo "  Node.js: $(node -v)"

# === УСТАНОВКА OPENCLAW ===
echo "✓ Установка OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    npm install -g openclaw@latest
fi
echo "  OpenClaw: $(openclaw --version)"

# === ГЕНЕРАЦИЯ ТОКЕНОВ ===
GATEWAY_TOKEN="${OPENCLAW_GATEWAY_TOKEN:-$(openssl rand -hex 32)}"

# === ОПРЕДЕЛЕНИЕ AUTH PROVIDER ===
AUTH_CHOICE="skip"
AUTH_FLAGS=""

if [ -n "$ANTHROPIC_API_KEY" ]; then
    AUTH_CHOICE="anthropic-api-key"
    AUTH_FLAGS="--anthropic-api-key $ANTHROPIC_API_KEY"
elif [ -n "$OPENAI_API_KEY" ]; then
    AUTH_CHOICE="openai-api-key"
    AUTH_FLAGS="--openai-api-key $OPENAI_API_KEY"
elif [ -n "$OLLAMA_API_KEY" ]; then
    AUTH_CHOICE="custom-api-key"
    AUTH_FLAGS="--custom-provider-id ollama --custom-base-url https://ollama.com/v1 --custom-compatibility openai"
    # Первичная модель если не указана
    if [ -z "$OLLAMA_MODELS" ]; then
        echo "⚠️  OLLAMA_MODELS не указан. Используется 'glm-5' по умолчанию."
        echo "   Установи OLLAMA_MODELS='model1,model2' для явного списка."
        AUTH_FLAGS="$AUTH_FLAGS --custom-model-id glm-5"
    else
        # Берём первую модель как primary
        FIRST_MODEL=$(echo "$OLLAMA_MODELS" | cut -d',' -f1)
        AUTH_FLAGS="$AUTH_FLAGS --custom-model-id $FIRST_MODEL"
    fi
elif [ -n "$CUSTOM_BASE_URL" ]; then
    AUTH_CHOICE="custom-api-key"
    AUTH_FLAGS="--custom-provider-id ${CUSTOM_PROVIDER_ID:-custom} --custom-base-url $CUSTOM_BASE_URL --custom-compatibility openai"
    [ -n "$CUSTOM_MODEL_ID" ] && AUTH_FLAGS="$AUTH_FLAGS --custom-model-id $CUSTOM_MODEL_ID"
fi

# === ONBOARDING ===
echo "✓ Конфигурация OpenClaw..."
openclaw onboard \
    --non-interactive \
    --accept-risk \
    --mode local \
    --flow quickstart \
    --workspace "$OPENCLAW_WORKSPACE" \
    --gateway-bind "$OPENCLAW_GATEWAY_BIND" \
    --gateway-port "$OPENCLAW_GATEWAY_PORT" \
    --gateway-auth token \
    --gateway-token "$GATEWAY_TOKEN" \
    --auth-choice "$AUTH_CHOICE" \
    $AUTH_FLAGS \
    --install-daemon \
    --skip-channels \
    --skip-skills \
    --skip-ui

# === TELEGRAM (если есть токен) ===
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "✓ Настройка Telegram..."
    jq --arg token "$TELEGRAM_BOT_TOKEN" \
        '.channels.telegram.enabled = true | .channels.telegram.token = $token' \
        ~/.openclaw/openclaw.json > ~/.openclaw/openclaw.json.tmp
    mv ~/.openclaw/openclaw.json.tmp ~/.openclaw/openclaw.json
fi

# === OLLAMA CLOUD: Отдельный провайдер с openai-completions ===
# ⚠️ Важно: api: "ollama" добавляет /api → /api/api/chat (404)
# Решение: отдельный провайдер "ollama-cloud" с api: "openai-completions"
if [ -n "$OLLAMA_API_KEY" ] && [ -n "$OLLAMA_MODELS" ]; then
    echo "✓ Настройка Ollama Cloud (openai-completions provider)..."
    
    # Парсим модели в JSON массив
    MODELS_JSON=$(echo "$OLLAMA_MODELS" | tr ',' '\n' | while read model; do
        [ -z "$model" ] && continue
        echo "{\"id\": \"$model\", \"name\": \"$model\", \"reasoning\": true, \"input\": [\"text\"], \"cost\": {\"input\": 0, \"output\": 0}, \"contextWindow\": 131072, \"maxTokens\": 32768}"
    done | jq -s '.')
    
    FIRST_MODEL=$(echo "$OLLAMA_MODELS" | cut -d',' -f1)
    
    # Создаём отдельный провайдер ollama-cloud (НЕ ollama!)
    # Используем openai-completions для /v1/chat/completions endpoint
    jq --argjson models "$MODELS_JSON" --arg primary "ollama-cloud/$FIRST_MODEL" \
        '.models.providers["ollama-cloud"] = {
            "baseUrl": "https://ollama.com/v1",
            "apiKey": "${OLLAMA_API_KEY}",
            "api": "openai-completions",
            "models": $models
        } |
        .agents.defaults.model.primary = $primary |
        .agents.defaults.model.fallbacks = []' \
        ~/.openclaw/openclaw.json > ~/.openclaw/openclaw.json.tmp
    mv ~/.openclaw/openclaw.json.tmp ~/.openclaw/openclaw.json
    
    # Добавляем модели в agents.defaults.models для переключения через /model
    for model in $(echo "$OLLAMA_MODELS" | tr ',' ' '); do
        jq --arg model "ollama-cloud/$model" \
            '.agents.defaults.models[$model] = {}' \
            ~/.openclaw/openclaw.json > ~/.openclaw/openclaw.json.tmp
        mv ~/.openclaw/openclaw.json.tmp ~/.openclaw/openclaw.json
    done
    
    # Добавляем API ключ в systemd service (user service НЕ поддерживает EnvironmentFile)
    if ! grep -q "OLLAMA_API_KEY" ~/.config/systemd/user/openclaw-gateway.service 2>/dev/null; then
        sed -i "/^\[Service\]/a Environment=OLLAMA_API_KEY=$OLLAMA_API_KEY" ~/.config/systemd/user/openclaw-gateway.service
    fi
    
    echo "  Провайдер: ollama-cloud"
    echo "  API: openai-completions"
    echo "  Модели: $OLLAMA_MODELS"
fi

# === ЗАПУСК ===
echo "✓ Запуск Gateway..."
systemctl --user daemon-reload
systemctl --user enable openclaw-gateway
systemctl --user start openclaw-gateway

# === ПРОВЕРКА ===
echo ""
echo "✓ Проверка..."
sleep 3
if systemctl --user is-active openclaw-gateway &> /dev/null; then
    echo "✅ OpenClaw Gateway запущен!"
else
    echo "❌ Gateway не запущен. Проверь логи:"
    echo "   journalctl --user -u openclaw-gateway -n 50"
    exit 1
fi

# === ИТОГИ ===
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ OpenClaw установлен!"
echo ""
echo "📁 Конфиг: ~/.openclaw/openclaw.json"
echo "📁 Workspace: $OPENCLAW_WORKSPACE"
echo "🔑 Gateway Token: $GATEWAY_TOKEN"
echo ""
echo "🌐 Доступ:"
echo "   Local: http://127.0.0.1:$OPENCLAW_GATEWAY_PORT/"
echo "   Remote: ssh -L 18789:127.0.0.1:18789 user@vps"
echo ""
echo "📋 Команды:"
echo "   Статус: openclaw status"
echo "   Логи:   journalctl --user -u openclaw-gateway -f"
echo "   Doctor: openclaw doctor"
echo "════════════════════════════════════════════════════════════"
```

**Использование:**

```bash
# С Anthropic
ANTHROPIC_API_KEY=sk-... ./openclaw-vps-install.sh

# С OpenAI
OPENAI_API_KEY=sk-... ./openclaw-vps-install.sh

# С Ollama Cloud (ВАЖНО: укажи модели явно!)
OLLAMA_API_KEY=ollama-... OLLAMA_MODELS="glm-5,gpt-oss:120b" ./openclaw-vps-install.sh

# Без API ключа (настроить позже)
./openclaw-vps-install.sh
```

**⚠️ Ollama Cloud ВАЖНО — правильная конфигурация:**

**Проблема:** `api: "ollama"` добавляет `/api` к baseUrl → `/api/api/chat` (404)

**Решение:** Создать отдельный провайдер `ollama-cloud` с OpenAI-совместимым API:

```json
{
  "models": {
    "providers": {
      "ollama-cloud": {
        "baseUrl": "https://ollama.com/v1",
        "apiKey": "${OLLAMA_API_KEY}",
        "api": "openai-completions",
        "models": [
          {"id": "glm-5", "name": "GLM-5", "reasoning": true, "input": ["text"], "cost": {"input": 0, "output": 0}, "contextWindow": 200000, "maxTokens": 131072},
          {"id": "minimax-m2.5", "name": "MiniMax M2.5", "reasoning": true, "input": ["text"], "cost": {"input": 0, "output": 0}, "contextWindow": 200000, "maxTokens": 131072},
          {"id": "gemini-3-flash-preview", "name": "Gemini 3 Flash", "reasoning": true, "input": ["text"], "cost": {"input": 0, "output": 0}, "contextWindow": 131072, "maxTokens": 8192}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama-cloud/glm-5",
        "fallbacks": ["ollama-cloud/minimax-m2.5", "ollama-cloud/gemini-3-flash-preview"]
      },
      "models": {
        "ollama-cloud/glm-5": {"alias": "GLM-5"},
        "ollama-cloud/minimax-m2.5": {"alias": "MiniMax"},
        "ollama-cloud/gemini-3-flash-preview": {"alias": "Gemini"}
      }
    }
  }
}
```

**Ключевые моменты:**
1. **Провайдер:** `ollama-cloud` (не `ollama`) — чтобы избежать конфликта с нативным Ollama API
2. **API:** `openai-completions` — использует `/v1/chat/completions` endpoint
3. **baseUrl:** `https://ollama.com/v1` — OpenAI-совместимый endpoint
4. **Модели в `agents.defaults.models`** — обязательно для переключения через `/model`

**Получить список моделей Ollama Cloud:**
```bash
curl -H "Authorization: Bearer $OLLAMA_API_KEY" https://ollama.com/api/tags | jq '.models[].name'
```

**Systemd + OLLAMA_API_KEY:**
User service НЕ поддерживает `EnvironmentFile`. Добавляй переменные напрямую:
```ini
[Service]
Environment=OLLAMA_API_KEY=your-key-here
```

---

## Ollama Web Search CLI

Ollama Cloud API включает веб-поиск через `/api/web_search` endpoint. Установка CLI:

```bash
# Создаём директорию и скрипт
mkdir -p ~/.openclaw/workspace/skills/ollama-web-search
curl -o ~/.openclaw/workspace/skills/ollama-web-search/ollama_web.py \
  https://raw.githubusercontent.com/dmitreshel-art/agent_skills/main/ollama-web-search/ollama_web.py
chmod +x ~/.openclaw/workspace/skills/ollama-web-search/ollama_web.py

# Линкуем в /usr/local/bin
sudo ln -sf ~/.openclaw/workspace/skills/ollama-web-search/ollama_web.py /usr/local/bin/ollama-web

# Проверяем
ollama-web search "test" --max 2
```

**Использование:**
```bash
# Поиск в интернете
ollama-web search "Python asyncio tutorial" --max 5
ollama-web search "AI news" --format json

# Загрузка страницы
ollama-web fetch https://docs.ollama.com
ollama-web fetch example.com --format markdown
```

**Преимущества vs Brave/Perplexity:**
- Бесплатно с Ollama Cloud API ключом
- Не нужен отдельный API ключ
- Работает через тот же `OLLAMA_API_KEY`

---

### Шаг 7: Systemd Daemon

OpenClaw имеет встроенную установку daemon:

```bash
# Установка systemd сервиса (через onboard)
openclaw onboard --install-daemon

# Или вручную
openclaw gateway install
```

**Ручное создание systemd user unit:**

```bash
# Создай systemd user service
mkdir -p ~/.config/systemd/user/

cat > ~/.config/systemd/user/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
ExecStart=%h/.npm-global/bin/openclaw gateway start
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# Активация
systemctl --user daemon-reload
systemctl --user enable openclaw-gateway
systemctl --user start openclaw-gateway

# Для запуска без логина
sudo loginctl enable-linger $USER
```

**System service (для VPS):**

```bash
sudo tee /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=openclaw
Group=openclaw
WorkingDirectory=/home/openclaw
Environment="NODE_ENV=production"
ExecStart=/usr/bin/openclaw gateway start --bind lan --port 18789
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-gateway

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/openclaw/.openclaw

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable openclaw-gateway
sudo systemctl start openclaw-gateway
```

### Шаг 8: Проверка

```bash
# Полная проверка
openclaw doctor

# Статус Gateway
openclaw status

# Глубокая проверка
openclaw status --deep

# Логи
journalctl -u openclaw-gateway -f
# Или для user service:
journalctl --user -u openclaw-gateway -f
```

### Шаг 9: Remote Access

**По умолчанию Gateway bind на loopback (127.0.0.1).**

#### Вариант A: SSH Tunnel (рекомендуется для одиночного доступа)

```bash
# На локальной машине
ssh -N -L 18789:127.0.0.1:18789 user@vps-ip

# Открой в браузере
# http://127.0.0.1:18789/
```

#### Вариант B: Nginx Reverse Proxy (для публичного доступа)

```bash
sudo apt install -y nginx certbot python3-certbot-nginx

# Конфигурация
sudo tee /etc/nginx/sites-available/openclaw << 'EOF'
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        proxy_buffering off;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# SSL сертификат
sudo certbot --nginx -d your-domain.com
```

**Важно для CORS:**
Добавь в `~/.openclaw/openclaw.json`:
```json
{
  "gateway": {
    "controlUi": {
      "allowedOrigins": ["https://your-domain.com"]
    }
  }
}
```

### Шаг 10: Control UI

После настройки доступа:

1. Открой в браузере: `https://your-domain.com/`
2. Введи токен из конфига или открой: `https://your-domain.com/#token=<TOKEN>`
3. Токен находится в `~/.openclaw/openclaw.json` → `gateway.auth.token`

**Или локально через SSH:**
```bash
ssh -N -L 18789:127.0.0.1:18789 user@vps
# Открой http://localhost:18789/
```

### Шаг 11: Telegram (опционально)

```bash
# Добавь в конфиг
openclaw configure --section channels

# Или вручную в openclaw.json:
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist"
    }
  }
}

# Рестарт
systemctl --user restart openclaw-gateway
```

### Шаг 12: SSH Hardening

```bash
# Только после проверки что SSH-ключи работают!
sudo nano /etc/ssh/sshd_config

# Изменить:
PasswordAuthentication no
PermitRootLogin no

# Перезапуск
sudo systemctl restart sshd
```

⚠️ **Не закрывай текущую SSH-сессию пока не проверишь вход по ключу!**

---

## Конфигурация

### Переменные окружения

OpenClaw использует переменные с префиксом `OPENCLAW_`:

| Переменная | Описание |
|------------|----------|
| `OPENCLAW_HOME` | Базовая директория (~/.openclaw) |
| `OPENCLAW_STATE_DIR` | Расположение mutable state |
| `OPENCLAW_CONFIG_PATH` | Путь к openclaw.json |
| `OPENCLAW_GATEWAY_PORT` | Порт Gateway (default: 18789) |
| `OPENCLAW_GATEWAY_BIND` | Bind address (loopback/lan/tailnet) |
| `OPENCLAW_GATEWAY_TOKEN` | Auth token |

### Credential Precedence

Из официальной документации:

1. **Explicit credentials** (`--token`, `--password`) — всегда приоритет
2. **Local mode defaults:**
   - token: `OPENCLAW_GATEWAY_TOKEN` → `gateway.auth.token` → `gateway.remote.token`
   - password: `OPENCLAW_GATEWAY_PASSWORD` → `gateway.auth.password`
3. **Remote mode defaults:**
   - token: `gateway.remote.token` → `OPENCLAW_GATEWAY_TOKEN` → `gateway.auth.token`

### Минимальный openclaw.json

```json
{
  "gateway": {
    "port": 18789,
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "<сгенерированный-токен>"
    },
    "controlUi": {
      "allowedOrigins": ["https://your-domain.com"]
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-3-5-sonnet"
      },
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist"
    }
  }
}
```

---

## Обновление

```bash
# Проверка версии
openclaw --version

# Обновление
npm update -g openclaw

# Рестарт сервиса
systemctl --user restart openclaw-gateway
# Или для system service:
sudo systemctl restart openclaw-gateway
```

**Автообновление (cron):**
```bash
# Ежедневно в 4:00
(crontab -l 2>/dev/null; echo "0 4 * * * npm update -g openclaw && systemctl --user restart openclaw-gateway") | crontab -
```

---

## Troubleshooting

### `openclaw: command not found`

```bash
# Проверь PATH
npm prefix -g
echo "$PATH"

# Добавь в ~/.bashrc или ~/.zshrc:
export PATH="$(npm prefix -g)/bin:$PATH"
```

### Gateway не запускается

```bash
# Логи
journalctl -u openclaw-gateway -n 50

# Ручной запуск для отладки
openclaw gateway start

# Проверка конфига
openclaw doctor
```

### Control UI не подключается (1006)

```bash
# Проверь bind
grep bind ~/.openclaw/openclaw.json
# Для VPS нужно "bind": "lan" или "bind": "0.0.0.0"

# Проверь что Gateway слушает
ss -tlnp | grep 18789
```

### Permission errors

```bash
# Проверь владельца
ls -la ~/.openclaw/
chown -R $USER:$USER ~/.openclaw
```

---

## Чек-лист безопасности

| Пункт | Команда | Ожидаемый результат |
|-------|---------|---------------------|
| UFW активен | `sudo ufw status` | `Status: active` |
| Только нужные порты | `sudo ufw status` | 22, 80, 443 |
| Gateway не публичен | `ss -tlnp \| grep 18789` | 127.0.0.1 или internal IP |
| Auth token установлен | `grep token ~/.openclaw/openclaw.json` | Есть токен |
| Sandbox включён | `grep sandbox ~/.openclaw/openclaw.json` | `"mode": "non-main"` |
| SSH ключи работают | `ssh -i ~/.ssh/key user@host` | Успешный вход |
| Password auth disabled | `grep PasswordAuthentication /etc/ssh/sshd_config` | `no` |

---

## Диагностика

```bash
# Полная проверка
openclaw doctor

# Статус
openclaw status

# Глубокий статус
openclaw status --deep

# Логи
journalctl -u openclaw-gateway -f

# Порты
ss -tlnp | grep 18789

# UFW
sudo ufw status verbose

# Nginx
sudo nginx -t
```

---

## Итоговый отчёт

```
✅ OpenClaw развёрнут (Native)!

📁 Данные:
   ~/.openclaw/
   ├── openclaw.json
   └── workspace/

🔒 Безопасность:
   • UFW: активен (22, 80, 443)
   • Gateway: loopback (доступ через SSH tunnel или Nginx)
   • Auth token: установлен
   • Sandbox: non-main

⚙️ Сервис:
   systemd: openclaw-gateway.service

🌐 Доступ:
   • Control UI: https://your-domain.com/#token=...
   • SSH tunnel: ssh -L 18789:127.0.0.1:18789 user@vps

📚 Документация:
   • Install: https://docs.openclaw.ai/install/
   • Remote: https://docs.openclaw.ai/gateway/remote
   • Security: https://docs.openclaw.ai/gateway/security
```