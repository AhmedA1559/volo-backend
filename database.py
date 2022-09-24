from firebase_admin import firestore

from model import Attendance

class Database:
    def __init__(self):
        self._client = firestore.client()

    def get_list_events_by_college(self, college_name: str):
        list_of_events_doc = self._client.collection('events').document(college_name).collection('list').get()

        return {'events': [event.to_dict() for event in list_of_events_doc]}

    def create_event_in_college(self, college_name: str, **kwargs):
        list_of_events_doc = self._client.collection('events').document(college_name).collection('list')
        # if the document doesn't exist, create it
        return list_of_events_doc.add(kwargs)

    def update_event_in_college(self, college_name: str, id: str, **kwargs):
        list_of_events_doc = self._client.collection('events').document(college_name).collection('list')
        list_of_events_doc.document(id).update(kwargs)

    def delete_event_in_college(self, college_name: str, id: str):
        list_of_events_doc = self._client.collection('events').document(college_name).collection('list')
        # if the document doesn't exist, create it
        list_of_events_doc.document(id).delete()

    def get_user(self, uid: str):
        user_doc = self._client.collection('users').document(uid).get()

        if user_doc.exists:
            return user_doc.to_dict()
        else:
            raise Exception("Could not find the given user.")

    def update_user_affiliation(self, uid: str, affiliation: str):
        user_doc = self._client.collection('users').document(uid)
        user_doc.update({affiliation: affiliation})

    def is_collaborator_by_uid(self, uid: str, college_name: str):
        user_doc = self._client.collection('users').document(uid).get()

        if user_doc.exists:
            return college_name in user_doc.to_dict()['collaborator']
        else:
            raise Exception("Could not find the given user.")

    def get_collaborators_by_college(self, college_name: str):
        list_of_collaborators_doc = self._client.collection('collaborators').document(college_name).collection('list').get()

        return {'list': list_of_collaborators_doc.to_dict()}

    def add_heartbeat_to_event(self, uid: str, id: str):
        attendance_ref = self._client.collection('attendance').document(id).get()

        if attendance_ref.exists:
            attendance = Attendance.from_dict(attendance_ref.to_dict())
            attendance.add_heartbeat(uid)
            self._client.collection('attendance').document(id).set(attendance.to_dict())
        else:
            attendance = Attendance().add_heartbeat(uid)
            self._client.collection('attendance').document(id).set(attendance.to_dict())

    def add_attending_to_event(self, uid: str, id: str):
        attendance_ref = self._client.collection('attendance').document(id).get()

        if attendance_ref.exists:
            attendance = Attendance.from_dict(attendance_ref.to_dict())
            attendance.add_attending(uid)
            self._client.collection('attendance').document(id).set(attendance.to_dict())
        else:
            attendance = Attendance().add_attending(uid)
            self._client.collection('attendance').document(id).set(attendance.to_dict())

    def remove_attending_from_event(self, uid: str, id: str):
        attendance_ref = self._client.collection('attendance').document(id).get()

        if attendance_ref.exists:
            attendance = Attendance.from_dict(attendance_ref.to_dict())
            attendance.remove_attending(uid)
            self._client.collection('attendance').document(id).set(attendance.to_dict())
        else:
            raise Exception("Could not find the given event.")

    def get_attendance_by_event(self, id: str):
        attendance_ref = self._client.collection('attendance').document(id).get()

        if attendance_ref.exists:
            return attendance_ref.to_dict()
        else:
            raise Attendance().to_dict()

    def get_users_in_college(self, college_name: str):
        list_of_users_doc = self._client.collection('users').where('affiliation', '==', college_name).get()

        return {'users': list_of_users_doc}
