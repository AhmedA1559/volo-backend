from datetime import datetime

class Attendance:
    def __init__(self, heartbeats: dict = {}, planning: list=[]):
        self.heartbeats = heartbeats
        self.planning = planning

    def to_dict(self):
        return {
            'heartbeats': self.heartbeats.__dict__,
            'planning': self.planning,
        }

    @staticmethod
    def from_dict(dict):
        return Attendance(dict['heartbeats'], dict['planning'])

    def add_heartbeat(self, uid):
        if uid not in self.heartbeats:
            self.heartbeats[uid] = []

        self.heartbeats[uid].append(datetime.now())

    def add_attending(self, uid):
        if uid not in self.planning:
            self.planning.append(uid)

    def remove_attending(self, uid):
        if uid in self.planning:
            self.planning.remove(uid)
