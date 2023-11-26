from enum import Enum


class RequestType(Enum):

    CREATE_DB = 'create_db'
    SET_DB_BY_ID = 'set_db_by_id'
    SET_DB_BY_NAME = 'set_db_by_name'
    GET_KEY_FROM_DB = 'get_key_from_db'
    SET_KEY_IN_DB = 'set_key_in_db'
    DEL_KEY_IN_DB = 'del_key_in_db'
