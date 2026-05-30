from __future__ import annotations

from datetime import datetime, timedelta

from flask import Flask, request, jsonify

import config


def create_app(db_client=None) -> Flask:
    db = db_client if db_client is not None else config.get_db()
    app = Flask(__name__)

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

    return app
