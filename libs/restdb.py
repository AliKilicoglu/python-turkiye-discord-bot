import requests
import json
import os


url = os.environ["RESTDB-URL"]

headers = {
    "content-type"  : "application/json",
    "x-apikey"      : os.environ["RESTDB-KEY"],
    "cache-control" : "no-cache"
    }

level_sheet = (0, 50, 200, 700, 5700, 20700, 70700)


class User:
    def __init__(self, fields):
        self.objid = fields["_id"]
        self.id = int(fields["userid"])
        self.xp = int(fields["level"])
        self.calc_level()
        self.discord = None

    def update(self):
        payload = json.dumps({"level":self.xp})
        response = requests.request("PUT", f"{url}/{self.objid}", data=payload, headers=headers)

    def calc_level(self):
        level = 0
        for i in level_sheet:
            if self.xp >= i: level += 1

        self.level = level
        return self.level


class UserList:
    def __init__(self, ls=list()):
        self.__list = ls

    def __getitem__(self, index):
        return self.__list[index]

    def __len__(self):
        return self.__list.__len__()

    def append(self, item):
        self.__list.append(item)

    def get_by_userid(self, userid):
        for user in self.__list:
            if user.id == userid:
                return user

    def get_by_discord(self, attr, val):
        for user in self.__list:
            if getattr(user.discord, attr) == val:
                return user

userlist = UserList()


def load_all():
    global userlist
    response = requests.request("GET", url, headers=headers)
    j = json.loads(response.text)

    for obj in j:
        u = userlist.get_by_userid(obj["userid"])
        if u:
            if u.xp < obj["level"]:
                u.xp = int(obj["level"])
                u.objid = obj["_id"]
        else:
            userlist.append(User(obj))
