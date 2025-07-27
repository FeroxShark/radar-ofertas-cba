from __future__ import annotations

from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import os
import json
from google.cloud import firestore


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

    return app
