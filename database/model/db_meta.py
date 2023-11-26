from functools import singledispatchmethod
from threading import Lock

from database.model.consts import CANNOT_GET_DB, DB_NOT_EXIST, OK


class DatabaseMeta(type):

    _id_counter = 0

    _dbs = []
    name_to_db = {}
    id_to_db = {}

    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            name = kwargs.get('name')
            if name in cls.name_to_db:
                return cls.name_to_db[name]

            _id = cls._id_counter
            kwargs['id'] = _id

            db = super().__call__(*args, **kwargs)

            cls._dbs.append(db)
            cls.name_to_db[name] = db
            cls.id_to_db[_id] = db

            cls._id_counter += 1

            return db

    @classmethod
    def db_names(cls):
        return [*cls.name_to_db]

    @classmethod
    def db_ids(cls):
        return [*cls.id_to_db]

    @classmethod
    def names_to_ids(cls):
        return {name: db.id for name, db in cls.name_to_db.items()}

    @classmethod
    def ids_to_names(cls):
        return {_id: db.name for _id, db in cls.id_to_db.items()}

    @singledispatchmethod
    @classmethod
    def get_database(cls, arg):
        return

    @get_database.register(str)
    def _(cls, db_name: str):
        return cls.name_to_db.get(db_name, DB_NOT_EXIST)

    @get_database.register(int)
    def _(cls, db_id: int):
        return cls.id_to_db.get(db_id, DB_NOT_EXIST)

    @singledispatchmethod
    @classmethod
    def delete_database(cls, arg):
        pass

    @classmethod
    def _del_db_by_name(cls, db_name: str):
        index = None
        for i, db_iter in enumerate(cls._dbs):
            if db_iter.name == db_name:
                index = i
                break
        if index is not None:
            del cls._dbs[index]

    @delete_database.register(str)
    def _(cls, db_name: str):
        with cls._lock:
            try:
                db_id = cls.name_to_db[db_name].id
                del cls.name_to_db[db_name]
                del cls.id_to_db[db_id]
                cls._del_db_by_name(db_name=db_name)
                return OK
            except KeyError:
                return DB_NOT_EXIST

    @delete_database.register(int)
    def _(cls, db_id: int):
        with cls._lock:
            try:
                db_name = cls.id_to_db[db_id].name
                del cls.name_to_db[db_name]
                del cls.id_to_db[db_id]
                cls._del_db_by_name(db_name=db_name)
                return OK
            except KeyError:
                return DB_NOT_EXIST
