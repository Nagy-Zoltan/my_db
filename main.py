from database.model.db import Database
from database.requests.get_request import GetRequest
from database.requests.set_request import SetRequest


db1 = Database(name='hello')
db2 = Database(name='world')
db3 = Database(name='hello')
db4 = Database(name='hello1')

db = Database.from_id(2)


req = GetRequest(db=db1, key='h')

db1.drop()

data = {
    'bar': {
        'hello': {
            'world': {
                'foo': 'baz'
            }
        }
    }
}

db1.load(data=data)

print(db1.data)

s_req = SetRequest(db=db1, key='lol', val={'xd': {'one': 1, 'two': None}})
s_req2 = SetRequest(db=db1, key='lol.xd.three.four.five.six.seven.eight', val='xdd')

s_req.execute()
print(db1.data)

s_req2.execute()
print(db1.data)
