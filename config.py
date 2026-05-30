"""Configuración central del proyecto.

Lee todo desde variables de entorno (con `.env` opcional vía python-dotenv) y
expone un cliente Firestore perezoso para evitar exigir credenciales al
importar los módulos.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# Telegram: TELEGRAM_TOKEN es el nombre preferido; TG_TOKEN se mantiene por
# compatibilidad con configuraciones existentes.
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") or os.environ.get("TG_TOKEN", "")

# Alertas / self-check
EMAIL_ALERT = os.environ.get("EMAIL_ALERT", "")
SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
STALE_DAYS = _int("STALE_DAYS", 2)

# Ranking
DEALS_DIR = Path(os.environ.get("DEALS_DIR", "deals"))
PRICE_WINDOW_DAYS = _int("PRICE_WINDOW_DAYS", 30)
TOP_N = _int("TOP_N", 20)


def get_db():
    """Crea un cliente Firestore de forma perezosa.

    Usa `FIREBASE_KEY` (JSON de service account) si está definido; si no, cae al
    cliente por defecto (credenciales de aplicación / GOOGLE_APPLICATION_CREDENTIALS).
    """
    from google.cloud import firestore

    raw = os.environ.get("FIREBASE_KEY")
    if raw:
        try:
            creds = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError("FIREBASE_KEY no es un JSON válido") from exc
        return firestore.Client.from_service_account_info(creds)
    return firestore.Client()
