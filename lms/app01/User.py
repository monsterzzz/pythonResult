class User:
    def __init__(self,uid,name,password,is_admin):
        self.uid = uid
        self.name = name
        self.password = password
        self.is_admin = is_admin

    def to_dict(self):
        dic = {}
        dic['uid'] = self.uid
        dic['name'] = self.name
        dic['password'] = self.password
        dic['is_admin'] = self.is_admin
        return dic