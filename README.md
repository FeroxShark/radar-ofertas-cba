# Radar Ofertas

Proyecto de ejemplo para detectar ofertas y notificarlas por Telegram.

## Desarrollo

```bash
make dev
make test
```

## Deploy a Railway

1. Crear un nuevo proyecto **Python 3.10**.
2. Definir variables de entorno necesarias (`TELEGRAM_TOKEN`, credenciales de Google, `EMAIL_ALERT`).
3. Habilitar GitHub Deploy y configurar un cron para ejecutar `python main.py scrape` y `python main.py rank` diariamente.
4. Para el bot y los webhooks, usar `python main.py bot --token $TELEGRAM_TOKEN` y `python main.py payment`.
