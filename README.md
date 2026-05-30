# Radar Ofertas

Bot de Telegram que scrapea precios de supermercados, rankea ofertas y notifica
a suscriptores, con webhooks de pago en Flask y datos en Firestore.

## Desarrollo

```bash
make dev    # instala dependencias
make test   # flake8 + pytest
```

## Comandos

```bash
python main.py scrape       # scrapea retailers y guarda precios en Firestore
python main.py rank         # genera el top de ofertas del día en DEALS_DIR
python main.py bot          # corre el bot de Telegram (polling)
python main.py payment      # levanta el servidor de webhooks de pago
python main.py self_check   # alerta si algún scraper quedó atrasado
```

## Variables de entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Token del bot (alias: `TG_TOKEN`) | — |
| `FIREBASE_KEY` | JSON del service account de Firebase | credenciales por defecto |
| `EMAIL_ALERT` | Email para alertas de `self_check` | — |
| `SMTP_HOST` | Host SMTP para enviar alertas | `localhost` |
| `DEALS_DIR` | Carpeta donde se escribe el top diario | `deals` |
| `PRICE_WINDOW_DAYS` | Ventana de precios para el ranking | `30` |
| `TOP_N` | Cantidad de ofertas en el top | `20` |
| `STALE_DAYS` | Días sin actividad para marcar scraper caído | `2` |

## Deploy a Railway

1. Crear un proyecto **Python 3.11**.
2. Definir las variables de entorno necesarias (al menos `TELEGRAM_TOKEN` y
   `FIREBASE_KEY`).
3. Configurar un cron diario para `python main.py scrape` y `python main.py rank`.
4. Para el bot y los webhooks: `python main.py bot` y `python main.py payment`.
