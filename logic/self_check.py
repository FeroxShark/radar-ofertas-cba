from __future__ import annotations

from datetime import datetime, timedelta
import logging
import smtplib
from email.message import EmailMessage

import config

logger = logging.getLogger(__name__)


def _notify(failed: list[str]) -> None:
    if not config.EMAIL_ALERT:
        logger.warning("Scrapers atrasados sin EMAIL_ALERT configurado: %s", failed)
        return
    msg = EmailMessage()
    msg['From'] = config.EMAIL_ALERT
    msg['To'] = config.EMAIL_ALERT
    msg['Subject'] = '[Radar] Scraper failure'
    msg.set_content(', '.join(failed))
    try:
        with smtplib.SMTP(config.SMTP_HOST) as s:
            s.send_message(msg)
    except OSError as exc:
        logger.error(
            "No se pudo enviar la alerta por SMTP (%s): %s", config.SMTP_HOST, exc
        )


def run() -> None:
    """Alerta si algún scraper no registra actividad reciente."""
    db = config.get_db()
    threshold = datetime.utcnow() - timedelta(days=config.STALE_DAYS)
    failed = [
        scraper.id
        for scraper in db.collection('scraper_logs').stream()
        if (last_ts := scraper.get('ts')) and last_ts < threshold
    ]
    if failed:
        _notify(failed)
