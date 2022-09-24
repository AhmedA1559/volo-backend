from flask import Flask, jsonify
from firebase_admin import credentials, firestore, initialize_app
import os

app = Flask(__name__)

initialize_app(
    credential=credentials.Certificate({
        "type": os.environ.get('type'),
        "project_id": os.environ.get('project_id'),
        "private_key_id": os.environ.get('private_key_id'),
        "private_key": os.environ.get('private_key').replace('\\n', '\n'),
        "client_email": os.environ.get('client_email'),
        "client_id": os.environ.get('client_id'),
        "auth_uri": os.environ.get('auth_uri'),
        "token_uri": os.environ.get('token_uri'),
        "auth_provider_x509_cert_url": os.environ.get('auth_provider_x509_cert_url'),
        "client_x509_cert_url": os.environ.get('client_x509_cert_url')}
    )
)

db = firestore.client()
db_ref = db.collection('events')


@app.route('/')
def index():
    db_ref.document('test').set({'test': 'test'})
    return jsonify({"payload": db_ref.document('test').get().to_dict()}), 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
