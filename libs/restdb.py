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
        self.level = 1
        self.level_updated = False
        self.calc_level()
        self.discord = None

    def update(self):
        if self.objid is None: self.get_objid()
        self.calc_level()
        payload = json.dumps({"level":self.xp})
        requests.request("PUT", f"{url}/{self.objid}", data=payload, headers=headers)

    def delete(self):
        global userlist
        if self.objid is None: self.get_objid()
        requests.request("DELETE", f"{url}/{self.objid}", headers=headers)
        userlist.remove(self)

    def get_objid(self):
        response = requests.request("GET", url, headers=headers)
        j = json.loads(response.text)
        for obj in j:
            if int(obj["userid"]) == self.id:
                self.objid = obj["_id"]
                return

        print(f"Hata: {self.id} ID'li kullanıcı veritabanında bulunamadı")

    def calc_level(self):
        level = 0
        for i in level_sheet:
            if self.xp >= i: level += 1

        if level != self.level: self.level_updated = False
        self.level = level
        return self.level

    def pre_xp(self):
        for i, level in enumerate(level_sheet[::-1]):
            if self.xp == level:
                if i == 0: return 0
                return level_sheet[i-1]

            elif self.xp > level:
                return level

    def next_xp(self):
        for i, level in enumerate(level_sheet):
            if self.xp == level:
                if i == 6: return level
                return level_sheet[i+1]

            elif self.xp < level:
                return level


class UserList:
    def __init__(self, ls=list()):
        self.__list = ls

    def __getitem__(self, index):
        return self.__list[index]

    def __len__(self):
        return self.__list.__len__()

    def append(self, item):
        self.__list.append(item)

    def remove(self, item):
        self.__list.remove(item)

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

def new_user(userid):
    global userlist
    payload = json.dumps({"userid":userid,"level":0})
    response = requests.request("POST", url, data=payload, headers=headers)
    userlist.append(User({"_id":None, "userid":userid, "level":0}))
