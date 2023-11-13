
from db.schemas import getUsersDB

db = getUsersDB()

for i in db:
    #print(i)
    if "hello" == db[i]["display_name"]:
        #print(db[i]["exercise_plans"])
        for j in range(len(db[i]["exercise_plans"])):
            if "Pushups" == db[i]["exercise_plans"][j]["exercise_name"]:
                print(db[i]["exercise_plans"][j]["exercise_name"])