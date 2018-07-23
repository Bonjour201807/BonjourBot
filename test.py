import redis
# import time
#
# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# r = redis.Redis(connection_pool=pool)
# a = {'a':1,'b':2,'c':3}
# b = {'a':2,'b':2,'c':2}
# c = {'a':3,'b':2,'c':1}
# d = []
#
# name = 'as'
#
# print(r.lrange(name,start=0,end=100))
# r.lpush(name,a)
# r.lpush(name,b)
# r.lpush(name,c)
# r.delete(name)


from bonjour.nlu.nlu import NLU
from bonjour.dm.dst.dst import DST
from bonjour.agent.run_task import RunTask

policy_handle = RunTask()
while 1:
    u_input = input('user: ')
    print('bonjour: ', policy_handle.run({'query': u_input, 'uid': 'b'}))

