from flask import Flask, jsonify, request
from firebase_admin import credentials, firestore, initialize_app
import os

from database import Database
from middleware.auth import auth_required

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
app.config['db'] = Database()

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    return jsonify({}), 200


@app.route('/events/<college_name>')
@auth_required
def events_by_college(uid, college_name):
    if request.method == 'GET':
        return jsonify(app.config['db'].get_list_events_by_college(college_name)), 200
    elif request.method == 'POST':
        if app.config['db'].is_collaborator_by_uid(uid, college_name):
            return jsonify({'created_id': app.config['db'].create_event_in_college(college_name, **request.json)}), 200
        else:
            return jsonify({'error': 'You do not have the permission to create this.'}), 401
    return jsonify({}), 405


@app.route('/events/<college_name>/<id>')
@auth_required
def update_event_in_college(uid, college_name, id):
    if request.method == 'PUT':
        if app.config['db'].is_collaborator_by_uid(uid, college_name):
            app.config['db'].update_event_in_college(college_name, id, **request.json)
            return jsonify({}), 200
        else:
            return jsonify({'error': 'You do not have the permission to update this.'}), 401
    elif request.method == 'DELETE':
        if app.config['db'].is_collaborator_by_uid(uid, college_name):
            app.config['db'].delete_event_in_college(college_name, id)
            return jsonify({}), 200
        else:
            return jsonify({'error': 'You do not have the permission to delete this.'}), 401
    return jsonify({}), 405


@app.route('/collaborators/<college_name>')
@auth_required
def get_list_collaborators_by_college(uid, college_name):
    return jsonify(app.config['db'].get_collaborators_by_college(college_name)), 200


@app.route('/users/<uid>')
@auth_required
def get_user_by_uid(auth_uid, user_uid):
    if request.method == 'GET':
        return jsonify(app.config['db'].get_user(user_uid)), 200
    elif request.method == 'PUT':
        if auth_uid == user_uid:
            app.config['db'].update_user_affiliation(user_uid, request.json['affiliation'])
            return jsonify({}), 200
        else:
            return jsonify({'error': 'You do not have the permission to update this.'}), 401
    return jsonify({}), 405


@app.route('/attendance/<id>')
@auth_required
def attendance_by_event(uid, id):
    if request.method == 'GET':
        return jsonify(app.config['db'].get_attendance_by_event(id)), 200
    elif request.method == 'POST':
        app.config['db'].add_attending(uid, id)
        return jsonify({}), 200
    elif request.method == 'PUT':
        app.config['db'].add_heartbeat(uid, id)
        return jsonify({}), 200
    elif request.method == 'DELETE':
        app.config['db'].remove_attending(uid, id)
        return jsonify({}), 200
    return jsonify({}), 405


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
