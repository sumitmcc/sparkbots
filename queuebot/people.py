import json
import os
import pprint

from app import logger
from config import PEOPLE_FILE


class PeopleManager:
    def __init__(self, api, project):
        self._api = api
        self._file = PEOPLE_FILE.format(project)
        self._project = project

        os.makedirs(os.path.dirname(os.path.realpath(self._file)), exist_ok=True)

        if not os.path.exists(self._file):
            self._people = []
        else:
            self._people = json.load(open(self._file, 'r'))

    def get_people(self):
        return self._people

    def get_person(self, id):
        for person in self._people:
            if id == person['sparkId']:
                return person
        else:
            return {}

    def _save(self):
        json.dump(self._people, open(self._file, 'w'), indent=4, separators=(',', ': '))

    def update_person(self, id, **kwargs):
        person = self.get_person(id=id)
        for key, value in kwargs.items():
            person[key] = value
        self._save()

    def add_person(self, data):
        person = self.get_person(id=data['personId'])
        if not person:
            api_person = self._api.people.get(data['personId'])
            logger.debug("Adding person '" + data['personId'] + "'")

            person = {
                'sparkId': data['personId'],
                'displayName': api_person.displayName,
                'nickName': getattr(api_person, 'nickName', None),
                'lastName': api_person.lastName,
                'email': api_person.emails[0],
                'avatar': api_person.avatar,
                'project': self._project,
                'totalTimeInQueue': 0,  # microseconds
                'totalTimeAtHead': 0,  # microseconds
                'currentlyInQueue': False,  # microseconds
                'admin': False,
                'commands': 0,
                'number_of_times_in_queue': 0,
                'added_to_queue': [],
                'removed_from_queue': []
            }
            self._people.append(person)
            self._save()
            return person
        else:
            logger.info("Person '" + data['personId'] + "' not added because they already exist")
            return person
