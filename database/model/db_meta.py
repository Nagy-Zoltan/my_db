from threading import Lock


class DatabaseMeta(type):

    _dbs = []
    name_to_db = {}
    id_to_db = {}

    _create_lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._create_lock:
            name = kwargs.get('name')
            if name in cls.name_to_db:
                return cls.name_to_db[name]

            _id = len(cls._dbs)
            kwargs['id'] = _id

            db = super().__call__(*args, **kwargs)

            cls._dbs.append(db)
            cls.name_to_db[name] = db
            cls.id_to_db[_id] = db

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