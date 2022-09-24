from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app
import os

from database import Database
from middleware.auth import auth_required

app = Flask(__name__)
app.config['db'] = Database()
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


@app.route('/')
def index():
    return jsonify({}), 200

@app.route('/events/<college_name>', methods=['GET'])
def get_list_events_by_college(college_name):
    return jsonify(app.config['db'].get_list_events_by_college(college_name)), 200

@app.route('/events/<college_name>', methods=['POST'])
@auth_required
def create_event_in_college(uid, college_name):
    if (app.config['db'].is_collaborator_by_uid(uid, college_name)):
        return jsonify({'created_id': app.config['db'].create_event_in_college(college_name, **request.json)}), 200
    else:
        return jsonify({'error': 'You do not have the permission to create this.'}), 401

@app.route('/events/<college_name>/<id>', methods=['PUT'])
@auth_required
def update_event_in_college(uid, college_name, id):
    if (app.config['db'].is_collaborator_by_uid(uid, college_name)):
        app.config['db'].update_event_in_college(college_name, id, **request.json)
        return jsonify({}), 200
    else:
        return jsonify({'error': 'You do not have the permission to update this.'}), 401

@app.route('/events/<college_name>/<id>', methods=['DELETE'])
@auth_required
def delete_event_in_college(uid, college_name, id):
    if (app.config['db'].is_collaborator_by_uid(uid, college_name)):
        app.config['db'].delete_event_in_college(college_name, id)
        return jsonify({}), 200
    else:
        return jsonify({'error': 'You do not have the permission to delete this.'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
