from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from google.cloud import firestore

from logic.rank import Deal


db = firestore.Client()


def _is_active(chat_id: int) -> bool:
    doc = db.collection('subs').document(str(chat_id)).get()
    if not doc.exists:
        return False
    exp = doc.get('exp_date')
    return exp and exp > datetime.utcnow()


def _load_today() -> list[Deal]:
    today = datetime.utcnow().date().isoformat()
    path = Path('deals') / f'{today}.json'
    if not path.exists():
        return []
    return [Deal(**d) for d in json.loads(path.read_text())]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bienvenido a Radar Ofertas')


async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_active(update.effective_chat.id):
        await update.message.reply_text('Suscripción vencida')
        return
    deals = _load_today()
    if not deals:
        await update.message.reply_text('Sin datos hoy')
        return
    lines = [f"{d.name} - {d.savings_pct:.1f}% {d.url}" for d in deals]
    await update.message.reply_text('\n'.join(lines))


async def producto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_active(update.effective_chat.id):
        await update.message.reply_text('Suscripción vencida')
        return
    query = ' '.join(context.args)
    deals = _load_today()
    query_lower = query.lower()
    found = min(
        (d for d in deals if query_lower in d.name.lower()),
        key=lambda d: d.price_unit,
        default=None,
    )
    if found:
        await update.message.reply_text(f"{found.name} {found.price_ars} - {found.url}")
    else:
        await update.message.reply_text('Sin resultados')


def run(token: str) -> None:
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('hoy', hoy))
    application.add_handler(CommandHandler('producto', producto))
    application.run_polling()
