from datetime import datetime
from typing import Any

from database.model.consts import INVALID_KEY, NOT_SET, OK
from database.model.db_meta import DatabaseMeta


class Database(metaclass=DatabaseMeta):

    def __init__(self, name: str, **kwargs):
        self._name = name
        self._id = kwargs.get('id')

        self.created_at = datetime.now()
        self.created_by = 'admin'

        self._data = {
            'hello': 'world',
            'foo': None,
            'bar': {
                'baz': [1, 2, 3],
                'hello': {
                    'world': [1, 2]
                }
            }
        }

    @classmethod
    def from_id(cls, _id):
        return cls.id_to_db[_id]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    def drop(self):
        self._data.clear()

    def load(self, data: dict):
        self._data = data

    def get_data(self, key: str):
        data = self._data
        split_key = key.split('.')
        for key in split_key:
            try:
                _data = data
                data = data.get(key)
            except AttributeError:
                return INVALID_KEY
            if data is None and key not in _data:
                return NOT_SET
        return data

    def set_data(self, key: str, val: Any):
        data = self._data
        split_key = key.split('.')

        for key in split_key[:-1]:
            try:
                _data = data
                data = data.get(key)
            except AttributeError:
                return 0, INVALID_KEY

            if data is None and key not in _data:
                data = _data[key] = {}

        last_key = split_key[-1]
        try:
            data[last_key] = val
            return 1, OK
        except TypeError:
            return 0, INVALID_KEY
