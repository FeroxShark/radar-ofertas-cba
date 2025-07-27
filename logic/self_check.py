from __future__ import annotations

from datetime import datetime, timedelta
from os import environ
import smtplib
from email.message import EmailMessage

from google.cloud import firestore


def run() -> None:
    """Placeholder self check."""
    db = firestore.Client()
    now = datetime.utcnow()
    threshold = now - timedelta(days=2)
    failed = []
    for scraper in db.collection('scraper_logs').stream():
        last_ts = scraper.get('ts')
        if last_ts and last_ts < threshold:
            failed.append(scraper.id)
    if failed:
        msg = EmailMessage()
        msg['From'] = environ.get('EMAIL_ALERT')
        msg['To'] = environ.get('EMAIL_ALERT')
        msg['Subject'] = '[Radar] Scraper failure'
        msg.set_content(', '.join(failed))
        with smtplib.SMTP('localhost') as s:
            s.send_message(msg)
