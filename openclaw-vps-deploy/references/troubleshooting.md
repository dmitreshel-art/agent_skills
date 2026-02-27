# Troubleshooting

## Подключение по SSH

### Ошибка: Permission denied (publickey)

**Причина:** SSH настроен только по ключу, но ключ не добавлен.

**Решение:**
```bash
# С локальной машины
ssh-copy-id openclaw@<IP>

# Или временно включить пароль (на сервере как root)
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd
```

### Ошибка: Connection refused

**Причина:** UFW блокирует SSH или SSH не запущен.

**Решение:**
```bash
# Проверь UFW
ufw status

# Разреши SSH
ufw allow ssh

# Проверь SSH
systemctl status sshd
```

---

## Docker

### Ошибка: permission denied

**Причина:** Пользователь не в группе docker.

**Решение:**
```bash
usermod -aG docker openclaw
# Перелогинься
su - openclaw
```

### Ошибка: Docker not found

**Причина:** Docker не установлен или не запущен.

**Решение:**
```bash
systemctl start docker
systemctl enable docker
docker ps
```

---

## OpenClaw Gateway

### Gateway не запускается

**Проверь логи:**
```bash
cd ~/openclaw-repo
docker compose logs openclaw-gateway
```

**Частые причины:**
- Нет API ключа → проверь `.env`
- Порт занят → `lsof -i :18789`
- Конфиг неверный → `openclaw doctor`

### Ошибка: unauthorized / pairing required

**Решение:**
```bash
# Получи токен
docker compose run --rm openclaw-cli dashboard --no-open

# Или добавь устройство
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

---

## Ollama Cloud

### Ошибка: API key invalid

**Проверь ключ:**
```bash
curl -s https://ollama.com/api/tags \
  -H "Authorization: Bearer $OLLAMA_API_KEY"
```

**Если ошибка 401 — сгенерируй новый ключ на https://ollama.com/settings/keys**

### Модели не появляются

**Проверь конфиг:**
```bash
docker compose run --rm openclaw-cli models list
```

**Если пусто — проверь `openclaw.json`:**
- `models.providers.ollama.apiKey` должен быть или в конфиге, или в `.env` как `OLLAMA_API_KEY`

---

## Память и Embeddings

### Ошибка: embedding model not found

**Причина:** Модель не скачалась.

**Решение:**
```bash
# Ручной запуск для скачивания
docker compose run --rm openclaw-cli memory index --verbose
```

### Memory search не работает

**Проверь:**
```bash
docker compose run --rm openclaw-cli memory status --deep
```

**Если `provider: none` — проверь конфиг `memorySearch.provider: "local"`**

---

## Nginx

### Ошибка: nginx: [emerg] host not found

**Причина:** Домен не резолвится на IP сервера.

**Решение:**
```bash
# Проверь DNS
dig YOUR_DOMAIN +short
nslookup YOUR_DOMAIN

# Должен вернуть IP твоего сервера
```

### Ошибка: SSL certificate failed

**Причина:** Certbot не может проверить домен.

**Решение:**
```bash
# Убедись что порт 80 открыт
ufw allow 80/tcp

# Проверь что Nginx запущен
systemctl status nginx

# Перезапусти certbot
certbot --nginx -d YOUR_DOMAIN --test-cert
```

---

## Telegram

### Бот не отвечает

**Проверь:**
```bash
# Токен добавлен?
docker compose run --rm openclaw-cli channels list

# Бот работает?
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"

# Перезапусти gateway
docker compose restart openclaw-gateway
```

---

## Backup

### Backup не запускается по cron

**Проверь cron:**
```bash
crontab -u openclaw -l

# Проверь логи
cat /var/log/openclaw-backup.log
```

**Ручной запуск:**
```bash
/home/openclaw/backup-openclaw.sh
```

---

## Полезные команды

```bash
# Статус всех сервисов
docker compose ps
systemctl status nginx
ufw status

# Логи OpenClaw
docker compose logs -f --tail 100

# Health check
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"

# Обновление OpenClaw
cd ~/openclaw-repo
git pull
./docker-setup.sh

# Полная переустановка
cd ~/openclaw-repo
docker compose down -v
./docker-setup.sh
```
