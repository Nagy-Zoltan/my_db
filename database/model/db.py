from datetime import datetime
from threading import Lock
from typing import Any

from database.model.consts import INVALID_KEY, NOT_SET, OK
from database.model.db_meta import DatabaseMeta


class Database(metaclass=DatabaseMeta):

    _lock = Lock()

    def __init__(self, name: str, **kwargs):
        self._name = name
        self._id = kwargs.get('id')

        self.created_at = datetime.now()
        self.created_by = 'admin'

        self._data = {}

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
        with self._lock:
            data = self._data
            split_key = key.split('.')

            for key in split_key[:-1]:
                try:
                    _data = data
                    data = data.get(key)
                except AttributeError:
                    return INVALID_KEY

                if data is None and key not in _data:
                    data = _data[key] = {}

            last_key = split_key[-1]
            try:
                data[last_key] = val
                return OK
            except TypeError:
                return INVALID_KEY

    def del_data(self, key: str):
        with self._lock:
            data = self._data
            split_key = key.split('.')

            for key in split_key[:-1]:
                try:
                    _data = data
                    data = data.get(key)
                except AttributeError:
                    return INVALID_KEY
                if data is None and key not in _data:
                    return NOT_SET
            last_key = split_key[-1]
            try:
                del data[last_key]
                return OK
            except KeyError:
                return NOT_SET
            except TypeError:
                return INVALID_KEY

    def __repr__(self):
        return f'Database(name={self._name}, id={self._id}, created_at={self.created_at}, created_by={self.created_by})'
