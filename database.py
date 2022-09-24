from datetime import datetime

from firebase_admin import firestore


class Database:
    def __init__(self):
        self._client = firestore.client()

    def get_list_events_by_college(self, college_name: str):
        list_of_events_doc = self._client.collection('events').document(college_name).collection('list').get()

        if list_of_events_doc.exists:
            return list_of_events_doc.to_dict()
        else:
            raise Exception("Could not find the given college's list. Perhaps it isn't a valid college?")

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

        if list_of_collaborators_doc.exists:
            return list_of_collaborators_doc.to_dict()
        else:
            raise Exception("Could not find the given college's list. Perhaps it isn't a valid college?")