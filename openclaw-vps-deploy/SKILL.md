---
name: openclaw-vps-deploy
description: Deploy OpenClaw on Ubuntu VPS with Docker Compose, security hardening, Ollama Cloud integration, sandbox, memory, and optional HTTPS/Telegram. Use when the user asks to deploy, install, or set up OpenClaw on a VPS, server, or remote machine.
---

# OpenClaw VPS Deploy (Docker-first)

Развёртывание OpenClaw на Ubuntu VPS через Docker Compose с безопасностью по статье https://open-claw.su/knowledge/security/vps/

## Архитектура

```
VPS (Ubuntu 22.04)
├── UFW Firewall (22, 80, 443 only)
├── Docker Engine
├── Nginx (reverse proxy) → https://domain.com
│   └── HTTP + WebSocket → Gateway :18789
└── OpenClaw Container (0.0.0.0:18789)
    ├── Gateway :18789 (HTTP + WebSocket)
    ├── Browser Control :18791
    └── Telegram polling
        ↑
Данные на хосте: /home/openclaw/.openclaw/
├── .env (права 600)
├── openclaw.json (sandbox: non-main, bind: lan)
└── workspace/
    ├── MEMORY.md
    └── memory/
```

## Workflow

### Шаг 1: Сбор данных

Спроси последовательно:
1. IP адрес VPS?
2. SSH пользователь и пароль/ключ?
3. Ollama API ключ? (https://ollama.com/api-keys)
4. Домен для HTTPS? (опционально, но рекомендуется для Control UI)
5. Telegram bot token? (опционально)

### Шаг 2: Подготовка VPS

```bash
# SSH подключение
ssh user@IP

# Создание пользователя openclaw
sudo useradd -m -s /bin/bash openclaw
sudo usermod -aG sudo,docker openclaw

# SSH ключ для openclaw
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

⚠️ **НЕ открывай порт 18789!** Доступ к gateway — только через Nginx.

### Шаг 4: Docker установка

```bash
# Установка Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker openclaw

# Применить группу без перелогина
newgrp docker
```

### Шаг 5: OpenClaw развёртывание

```bash
# Клонирование
git clone https://github.com/openclaw/openclaw.git /home/openclaw/openclaw-repo
chown -R openclaw:openclaw /home/openclaw/openclaw-repo

# Сборка образа
cd /home/openclaw/openclaw-repo
docker build -t openclaw:local .

# Создание директорий
mkdir -p /home/openclaw/.openclaw/workspace
chown -R 1000:1000 /home/openclaw/.openclaw
```

### Шаг 6: Конфигурация

**⚠️ Важно:** Секреты (API ключи, токены) храним в `.env`, НЕ в `openclaw.json`!

**openclaw.json** — `/home/openclaw/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "https://ollama.com",
        "api": "ollama",
        "models": []
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/glm-5"
      },
      "sandbox": {
        "mode": "non-main"
      }
    }
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "streaming": "off"
    }
  },
  "gateway": {
    "port": 18789,
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "<64-символьный-токен>"
    },
    "controlUi": {
      "allowedOrigins": ["https://your-domain.com"]
    }
  }
}
```

**Ключевые моменты:**
- `bind: "lan"` — Gateway слушает на 0.0.0.0 для доступа через Nginx
- `api: "ollama"` — нативный Ollama API (работает с Ollama Cloud)
- `models: []` — **пустой массив** для автообнаружения через `OLLAMA_API_KEY`
- `allowedOrigins` — домен для Control UI (CORS)
- `token` — генерируется: `openssl rand -hex 32`

**.env** — `/home/openclaw/openclaw-repo/.env`:

```bash
# Ollama Cloud API (автообнаружение моделей)
OLLAMA_API_KEY=<ollama_api_ключ>

# OpenClaw Gateway (дублирует openclaw.json)
GATEWAY_TOKEN=<gateway_token_из_openclaw.json>
SESSION_KEY=<случайная_строка_32_символа>

# Telegram (опционально)
TELEGRAM_BOT_TOKEN=<telegram_bot_token>
```

⚠️ **Права файла .env должны быть 600:**

```bash
chmod 600 /home/openclaw/openclaw-repo/.env
```

### Шаг 7: docker-compose.yml (порты для Nginx)

**Важно:** Для Control UI через HTTPS порты привязываются к 0.0.0.0!

```yaml
services:
  openclaw-gateway:
    image: openclaw:local
    container_name: openclaw-repo-openclaw-gateway-1
    restart: unless-stopped
    ports:
      - "18789:18789"    # Gateway (HTTP + WS) — для Nginx
      - "127.0.0.1:18790:18790"  # Bridge (loopback)
      - "127.0.0.1:18791:18791"  # Browser Control (loopback)
    volumes:
      - /home/openclaw/.openclaw:/home/node/.openclaw
      - /var/run/docker.sock:/var/run/docker.sock
    env_file:
      - .env
```

**Ключевые моменты:**
- `18789:18789` — Gateway доступен для Nginx (0.0.0.0)
- `127.0.0.1:18790/18791` — внутренние порты только loopback
- `env_file: .env` — все секреты из `.env` передаются в контейнер

### Шаг 8: Запуск

```bash
cd /home/openclaw/openclaw-repo
docker compose up -d

# Проверка портов
ss -tlnp | grep 18789
# Ожидаемый вывод: LISTEN ... 0.0.0.0:18789 ... (для Nginx)
```

### Шаг 9: Автообнаружение моделей

После запуска модели автоматически подгрузятся из Ollama Cloud:

```bash
# Проверка (в контейнере)
docker exec openclaw-repo-openclaw-gateway-1 node dist/index.js models list

# Если модели не появились — рестарт
docker compose restart
```

**Как это работает:**
1. `OLLAMA_API_KEY` в `.env` → передаётся в контейнер
2. OpenClaw опрашивает `https://ollama.com/api/tags`
3. Все модели с tool support появляются автоматически

### Шаг 10: Nginx + HTTPS (+ Control UI)

**Обязательно для Control UI!** Gateway требует HTTPS для корректной работы WebSocket.

```bash
sudo apt install -y nginx certbot python3-certbot-nginx

# Конфиг /etc/nginx/sites-available/openclaw
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

    # HTTP + WebSocket проксирование на Gateway
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

# SSL сертификат (до этого убедись что DNS настроен!)
sudo certbot --nginx -d your-domain.com
sudo systemctl reload nginx
```

**Важно:**
- `map $http_upgrade` — корректная обработка WebSocket
- `proxy_read_timeout 86400s` — долгие WebSocket соединения
- `allowedOrigins` в openclaw.json должен содержать `https://your-domain.com`

### Шаг 11: Control UI доступ

После настройки Nginx:

1. Открой в браузере: `https://your-domain.com/`
2. При первом подключении введи токен из `openclaw.json` → `gateway.auth.token`
3. Или открой сразу с токеном: `https://your-domain.com/#token=<TOKEN>`

**Альтернатива без домена — SSH туннель:**
```bash
ssh -L 18789:127.0.0.1:18789 user@vps-ip
# Затем открой http://localhost:18789/
```

### Шаг 12: Wrapper-скрипт

```bash
sudo tee /usr/local/bin/openclaw << 'EOF'
#!/bin/bash
cd /home/openclaw/openclaw-repo
if [ -t 0 ]; then
    docker compose exec openclaw-gateway node dist/index.js "$@"
else
    docker compose exec -T openclaw-gateway node dist/index.js "$@"
fi
EOF
sudo chmod +x /usr/local/bin/openclaw
```

### Шаг 13: Telegram (опционально)

Токен уже добавлен в `.env` как `TELEGRAM_BOT_TOKEN`. После рестарта:

```bash
# Проверка
docker exec openclaw-repo-openclaw-gateway-1 node dist/index.js status | grep Telegram
```

### Шаг 14: SSH Hardening (опционально, но рекомендуется)

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

## Чек-лист безопасности

После установки пройди по каждому пункту:

| Пункт | Команда проверки | Ожидаемый результат |
|-------|------------------|---------------------|
| Отдельный пользователь openclaw | `id openclaw` | `groups=sudo,docker` |
| UFW включён | `sudo ufw status` | `Status: active` |
| UFW: только 22, 80, 443 | `sudo ufw status` | Порты 22, 80, 443 |
| Порт 18789 закрыт от интернета | `sudo ufw status \| grep 18789` | Нет вывода |
| Docker работает | `docker ps` | Контейнер запущен |
| Gateway на lan | `ss -tlnp \| grep 18789` | `0.0.0.0:18789` |
| Sandbox включён | `grep sandbox ~/.openclaw/openclaw.json` | `"mode": "non-main"` |
| .env права 600 | `ls -la ~/openclaw-repo/.env` | `-rw-------` |
| Nginx проксирует WS | `sudo nginx -t` | `syntax is ok` |
| HTTPS сертификат | `sudo certbot certificates` | `VALID` |
| allowedOrigins настроен | `grep allowedOrigins ~/.openclaw/openclaw.json` | Ваш домен |
| Telegram работает | `curl -s "https://api.telegram.org/bot<TOKEN>/getMe"` | `"ok":true` |

---

## Итоговый отчёт

```
✅ OpenClaw развёрнут!

📁 Данные (персистентные):
   /home/openclaw/.openclaw/
   ├── .env (права 600)
   ├── openclaw.json (sandbox: non-main, bind: lan)
   └── workspace/

🔒 Безопасность:
   • UFW: активен (22, 80, 443)
   • Порт 18789: 0.0.0.0 (доступ через Nginx только)
   • Sandbox: non-main
   • .env: 600

🐳 Контейнер:
   openclaw-repo-openclaw-gateway-1

🌐 Доступ:
   • Control UI: https://your-domain.com/#token=...
   • Telegram: @bot (если подключён)

🔑 Токены:
   • Gateway: <из openclaw.json gateway.auth.token>
```

---

## Команды для диагностики

```bash
# Полная проверка
docker exec openclaw-repo-openclaw-gateway-1 node dist/index.js doctor

# Статус Gateway
docker exec openclaw-repo-openclaw-gateway-1 node dist/index.js status

# Логи
docker compose logs -f --tail 50

# Порты
ss -tlnp | grep 18789

# UFW статус
sudo ufw status verbose

# Nginx тест
sudo nginx -t

# WebSocket тест
curl -v -H "Upgrade: websocket" -H "Connection: Upgrade" \
  -H "Sec-WebSocket-Key: test" -H "Sec-WebSocket-Version: 13" \
  http://127.0.0.1:18789/ 2>&1 | head -5
# Ожидается: HTTP/1.1 400 или challenge JSON

# Telegram
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
```

---

## Обработка ошибок

| Проблема | Решение |
|----------|---------|
| SSH не подключается | Проверь IP, пользователя, пароль/ключ |
| UFW блокирует всё | `sudo ufw allow ssh` перед `enable` |
| Gateway не стартует | `docker compose logs` — проверить ошибки |
| Control UI не грузится | Проверь Nginx конфиг и `allowedOrigins` |
| WebSocket disconnect (1006) | Проверь `bind: "lan"` в openclaw.json |
| Unauthorized | Открой `https://domain.com/#token=<TOKEN>` |
| Telegram не подключается | Проверь токен: `curl https://api.telegram.org/bot<TOKEN>/getMe` |
| Ollama API ошибка | Проверь ключ: `curl https://ollama.com/api/tags -H "Authorization: Bearer $KEY"` |
| 502 Bad Gateway | Gateway не запущен или порт недоступен |
| Telegram не работает | `docker compose restart` после добавления токена |

---

## Решение проблем (детально)

### Control UI: Disconnected (1006)

**Симптомы:**
- UI открывается, но показывает "Disconnected (1006): no reason"
- WebSocket не подключается

**Диагностика:**
```bash
# 1. Проверь что Gateway слушает на 0.0.0.0
ss -tlnp | grep 18789
# Ожидается: 0.0.0.0:18789, НЕ 127.0.0.1:18789

# 2. Проверь bind в конфиге
grep '"bind"' ~/.openclaw/openclaw.json
# Ожидается: "bind": "lan"

# 3. Проверь WebSocket напрямую
curl -v -H "Upgrade: websocket" -H "Connection: Upgrade" \
  -H "Sec-WebSocket-Key: test" -H "Sec-WebSocket-Version: 13" \
  http://127.0.0.1:18789/ 2>&1 | head -5
# Ожидается: JSON с "connect.challenge" или HTTP/1.1 400
```

**Решение:**
1. Измени `bind: "lan"` в `openclaw.json`:
   ```json
   "gateway": {
     "port": 18789,
     "bind": "lan"
   }
   ```
2. Измени `docker-compose.yml` — убери `127.0.0.1` prefix:
   ```yaml
   ports:
     - "18789:18789"  # было "127.0.0.1:18789:18789"
   ```
3. Перезапусти: `docker compose down && docker compose up -d`

### Control UI: Unauthorized / gateway token missing

**Симптомы:**
- UI открывается, но просит токен
- После ввода токена: "Unauthorized" или "gateway token missing"

**Решение:**
1. Генерируй токен: `openssl rand -hex 32`
2. Добавь в `openclaw.json`:
   ```json
   "gateway": {
     "auth": {
       "mode": "token",
       "token": "<сгенерированный_токен>"
     }
   }
   ```
3. Открой URL с токеном: `https://your-domain.com/#token=<TOKEN>`
4. UI автоматически сохранит токен в localStorage

### Control UI: CORS / allowedOrigins error

**Симптомы:**
- Консоль браузера показывает CORS ошибки
- WebSocket соединение отклоняется

**Решение:**
Добавь `allowedOrigins` в `openclaw.json`:
```json
"gateway": {
  "controlUi": {
    "allowedOrigins": ["https://your-domain.com"]
  }
}
```

### Nginx: 502 Bad Gateway

**Симптомы:**
- Nginx возвращает 502
- Gateway запущен

**Диагностика:**
```bash
# Проверь логи Nginx
sudo tail -20 /var/log/nginx/error.log

# Проверь что Gateway отвечает
curl http://127.0.0.1:18789/ | head -5
# Ожидается: HTML (<!doctype html>...)
```

**Решение:**
1. Убедись что `bind: "lan"` в openclaw.json
2. Убедись что порт `18789:18789` без 127.0.0.1 prefix
3. Проверь Nginx конфиг — должен быть `proxy_pass http://127.0.0.1:18789`

### Nginx: WebSocket не работает

**Симптомы:**
- HTTP работает, WebSocket — нет
- UI грузится, но "Disconnected"

**Решение:**
Добавь в Nginx конфиг:
```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

server {
    # ... SSL конфиг ...

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        proxy_buffering off;
    }
}
```

**Ключевые моменты:**
- `map $http_upgrade` — обязателен для WebSocket
- `Connection $connection_upgrade` — не `"upgrade"` строкой, а переменная
- `proxy_read_timeout 86400s` — для долгих соединений

---

## Быстрое восстановление

```bash
# Перезапуск всего
cd /home/openclaw/openclaw-repo
docker compose down && docker compose up -d

# Перегенерация токена
NEW_TOKEN=$(openssl rand -hex 32)
# Обновить в openclaw.json и .env
docker compose restart

# Пересоздание SSL
sudo certbot renew --force-renewal
sudo systemctl reload nginx
```

---

## Ресурсы

- **Статья безопасности:** https://open-claw.su/knowledge/security/vps/
- **Официальная документация:** https://docs.openclaw.ai/
- **Docker установка:** https://docs.openclaw.ai/install/docker
- **Control UI:** https://docs.openclaw.ai/web/control-ui