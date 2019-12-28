import redis
import json

class UpdateToRedis:
    def add(self, key, dic):

        redis_obj = redis.Redis()

        redis_obj.set(key, str(dic))

    def normal_get(self, key):
        redis_obj = redis.Redis()
        data = redis_obj.get(str(key))
        return data

    def get_data(self, key):
        redis_obj = redis.Redis()
        data = redis_obj.get(str(key))
        dic_str = data.decode("utf-8")

        dic_str = dic_str.replace("\'", "\"")

        final_dic = json.loads(dic_str)
        return final_dic



