import re

from database.requests.create_db_request import CreateDBRequest
from database.requests.get_key_request import GetKeyRequest
from database.requests.request_type import RequestType
from database.requests.set_db_by_id_request import SetDBByIDRequest
from database.requests.set_db_by_name_request import SetDBByNameRequest
from database.requests.set_key_request import SetKeyRequest


class RequestParser:

    PATTERNS = {
        RequestType.CREATE_DB: re.compile(r'^[dD][bB] [cC][rR][eE][aA][tT][eE] \w+$'),
        RequestType.SET_DB_BY_ID: re.compile(r'^[dD][bB] [iI][dD] \d+$'),
        RequestType.SET_DB_BY_NAME: re.compile(r'^[dD][bB] [nN][aA][mM][eE] \w+$'),
        RequestType.GET_KEY_FROM_DB: re.compile(r'^[gG][eE][tT] \w[.\w]\w+$'),
        RequestType.SET_KEY_IN_DB: re.compile(r'^[sS][eE][tT] \w[.\w]+\w .+?$')
    }

    def get_request_type(self, request_string):
        for request_type, pattern in self.PATTERNS.items():
            if re.match(pattern, request_string):
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
            return GetKeyRequest(db=client.db, key=key_name)
        if request_type == RequestType.SET_KEY_IN_DB:
            key_name, val_name = request_string.split(maxsplit=2)[-2:]
            return SetKeyRequest(db=client.db, key=key_name, val=val_name)
