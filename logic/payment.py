from __future__ import annotations

from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import os
from telegram import Update
from telegram.ext import Application, CommandHandler
import json
from google.cloud import firestore

BOT_TOKEN = os.environ.get("TG_TOKEN", "")


def build_bot() -> Application:
    from bot.bot import start

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    return app


def create_app(db_client: firestore.Client | None = None) -> Flask:
    if db_client is None:
        creds = json.loads(os.environ["FIREBASE_KEY"])
        db_client = firestore.Client.from_service_account_info(creds)
    app = Flask(__name__)
    db = db_client

    @app.post('/webhook/mp')
    @app.post('/webhook/usdt')
    def webhook() -> tuple[str, int]:
        data = request.json or {}
        chat_id = data.get('chat_id')
        if chat_id:
            db.collection('subs').document(str(chat_id)).set(
                {'exp_date': datetime.utcnow() + timedelta(days=30)}, merge=True
            )
        return jsonify({'status': 'ok'}), 200

    @app.get('/healthz')
    def healthz() -> tuple[str, int]:
        return jsonify({'status': 'ok'}), 200

    @app.post(f"/bot/{BOT_TOKEN}")
    def telegram_webhook() -> tuple[str, int]:
        update = Update.de_json(request.get_json(force=True), build_bot().bot)
        build_bot().process_update(update)
        return jsonify({'status': 'ok'}), 200

    return app
