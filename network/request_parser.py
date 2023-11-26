import re

from database.requests.create_db_request import CreateDBRequest
from database.requests.del_key_request import DelKeyRequest
from database.requests.drop_db_by_name_request import DropDBByNameRequest
from database.requests.drop_db_by_id_request import DropDBByIDRequest
from database.requests.get_all_request import GetAllRequest
from database.requests.get_key_request import GetKeyRequest
from database.requests.request_type import RequestType
from database.requests.set_db_by_id_request import SetDBByIDRequest
from database.requests.set_db_by_name_request import SetDBByNameRequest
from database.requests.set_key_request import SetKeyRequest


class RequestParser:

    _KEY_PATTERN = r'\w+(\.\w+)*'

    PATTERNS = {
        RequestType.CREATE_DB: re.compile(r'^[dD][bB] [cC][rR][eE][aA][tT][eE] \w+$'),
        RequestType.SET_DB_BY_ID: re.compile(r'^[dD][bB] [iI][dD] \d+$'),
        RequestType.SET_DB_BY_NAME: re.compile(r'^[dD][bB] [nN][aA][mM][eE] \w+$'),
        RequestType.GET_KEY_FROM_DB: re.compile(fr'^[gG][eE][tT] {_KEY_PATTERN}$'),
        RequestType.SET_KEY_IN_DB: re.compile(fr'^[sS][eE][tT] {_KEY_PATTERN} .+?$'),
        RequestType.DEL_KEY_IN_DB: re.compile(fr'^[dD][eE][lL] {_KEY_PATTERN}$'),
        RequestType.GET_ALL_FROM_DB: re.compile(r'^[gG][eE][tT][aA][lL][lL]$'),
        RequestType.DROP_DB_BY_NAME: re.compile(r'^[dD][bB] [dD][rR][oO][pP] [nN][aA][mM][eE] \w+$'),
        RequestType.DROP_DB_BY_ID: re.compile(r'^[dD][bB] [dD][rR][oO][pP] [iI][dD] \d+$')
    }

    def get_request_type(self, request_string):
        for request_type, pattern in self.PATTERNS.items():
            if re.fullmatch(pattern, request_string):
                return request_type

    def get_request_obj(self, client, request_string: str):
        request_type = self.get_request_type(request_string=request_string)
        if request_type == RequestType.CREATE_DB:
            db_name = request_string.split(maxsplit=2)[-1]
            return CreateDBRequest(name=db_name)
        if request_type == RequestType.SET_DB_BY_ID:
            db_id = int(request_string.split(maxsplit=2)[-1])
            return SetDBByIDRequest(client=client, id_=db_id)
        if request_type == RequestType.SET_DB_BY_NAME:
            db_name = request_string.split(maxsplit=2)[-1]
            return SetDBByNameRequest(client=client, name=db_name)
        if request_type == RequestType.GET_KEY_FROM_DB:
            key_name = request_string.split(maxsplit=1)[-1]
            db = client.get_database()
            return GetKeyRequest(db=db, key=key_name)
        if request_type == RequestType.SET_KEY_IN_DB:
            key_name, val_name = request_string.split(maxsplit=2)[-2:]
            db = client.get_database()
            return SetKeyRequest(db=db, key=key_name, val=val_name)
        if request_type == RequestType.DEL_KEY_IN_DB:
            key_name = request_string.split(maxsplit=1)[-1]
            db = client.get_database()
            return DelKeyRequest(db=db, key=key_name)
        if request_type == RequestType.GET_ALL_FROM_DB:
            db = client.get_database()
            return GetAllRequest(db=db)
        if request_type == RequestType.DROP_DB_BY_NAME:
            db_name = request_string.split(maxsplit=3)[-1]
            return DropDBByNameRequest(name=db_name)
        if request_type == RequestType.DROP_DB_BY_ID:
            db_id = int(request_string.split(maxsplit=3)[-1])
            return DropDBByIDRequest(id_=db_id)
