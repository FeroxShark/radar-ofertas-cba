from __future__ import annotations

from datetime import datetime
from functools import wraps
import json

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import config
from logic.rank import Deal

_db = None


def _get_db():
    """Cliente Firestore perezoso (no exige credenciales al importar)."""
    global _db
    if _db is None:
        _db = config.get_db()
    return _db


def _is_active(chat_id: int) -> bool:
    doc = _get_db().collection('subs').document(str(chat_id)).get()
    if not doc.exists:
        return False
    exp = doc.get('exp_date')
    return exp and exp > datetime.utcnow()


def require_active_subscription(handler):
    """Responde 'Suscripción vencida' si el chat no tiene sub activa."""

    @wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not _is_active(update.effective_chat.id):
            await update.message.reply_text('Suscripción vencida')
            return
        await handler(update, context)

    return wrapper


def _load_today() -> list[Deal]:
    today = datetime.utcnow().date().isoformat()
    path = config.DEALS_DIR / f'{today}.json'
    if not path.exists():
        return []
    return [Deal(**d) for d in json.loads(path.read_text())]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bienvenido a Radar Ofertas')


@require_active_subscription
async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    deals = _load_today()
    if not deals:
        await update.message.reply_text('Sin datos hoy')
        return
    lines = [f"{d.name} - {d.savings_pct:.1f}% {d.url}" for d in deals]
    await update.message.reply_text('\n'.join(lines))


@require_active_subscription
async def producto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
