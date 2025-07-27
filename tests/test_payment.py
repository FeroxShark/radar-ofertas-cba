from datetime import datetime

from logic import payment


class DummyDoc:
    def __init__(self):
        self.data = None

    def set(self, data, merge=False):
        self.data = data


class DummyCollection:
    def __init__(self):
        self.doc = DummyDoc()

    def document(self, name):
        return self.doc


class DummyDB:
    def __init__(self):
        self.collection_obj = DummyCollection()

    def collection(self, name):
        return self.collection_obj


def test_webhook_updates_expiration():
    db = DummyDB()
    app = payment.create_app(db)
    client = app.test_client()
    resp = client.post('/webhook/mp', json={'chat_id': '123'})
    assert resp.status_code == 200
    assert db.collection_obj.doc.data['exp_date'] > datetime.utcnow()


def test_healthz_endpoint():
    db = DummyDB()
    app = payment.create_app(db)
    client = app.test_client()
    resp = client.get('/healthz')
    assert resp.status_code == 200
    assert resp.get_json() == {'status': 'ok'}
