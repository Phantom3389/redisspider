# _*_ encoding: utf-8 _*_
__author__ = 'Phantom3389'
__date__ = '2018/3/14 15:58'

import redis
from redisspider.settings import BF_REDIS_HOST, BF_REDIS_PORT, BF_REDIS_PARAMS

pool = redis.ConnectionPool(host=BF_REDIS_HOST, port=BF_REDIS_PORT, db=0, password=BF_REDIS_PARAMS['password'])
conn = redis.StrictRedis(connection_pool=pool)

pipline = conn.pipeline()
pipline.lrange("jobbole:items", 0, 3)
#default_decode = ScrapyJSONDecoder().decode()
result = pipline.execute()
#result1 = default_decode(result[0][0])
cookie = {}
cookie['test1'] = "test1"
cookie['test2'] = "test2"
print(len(result[0]))
print(result[0][1])