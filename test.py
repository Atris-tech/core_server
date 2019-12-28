import redis
import json


r = redis.Redis()

myDic = {
    "count_m" : 4,
    "count_c" : 2
}

r.set("c_check", str(myDic))



data = r.get("c_check")

print(data)

dic_str = data.decode("utf-8")

dic_str = dic_str.replace("\'", "\"")

final_dic = json.loads(dic_str)

print("*******************************")
i = 0
while i <= 5:
    final_dic["count_m"] = i
    r.set("c_check", str(final_dic))
    print(r.get("c_check"))
    i = i + 1

data1 = r.get("c_check")


