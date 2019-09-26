from engin import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(120))

class Cod(db.Model):
    __tablename__ = 'cods'
    id = db.Column(db.Integer,primary_key=True)
    time =  db.Column(db.String(64))
    data = db.Column(db.String(64))
    remark =  db.Column(db.String(255))

class Bod(db.Model):
    __tablename__ = 'bods'
    id = db.Column(db.Integer,primary_key=True)
    time =  db.Column(db.String(64))
    data = db.Column(db.String(64))
    remark =  db.Column(db.String(255))

class Ph(db.Model):
    __tablename__ = 'phs'
    id = db.Column(db.Integer,primary_key=True)
    time =  db.Column(db.String(64))
    data = db.Column(db.String(64))
    remark =  db.Column(db.String(255))

class Cctv(db.Model):
    __tablename__ = 'cctvs'
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(64),default="cctv")
    avatar = db.Column(db.String(255))
    port =  db.Column(db.String(64))

class Rcpt(db.Model):
    __tablename__ = 'rcpts'
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(64))
    number = db.Column(db.String(64))
    email = db.Column(db.String(255))

    def toJson(self):
        j = {
            "id" : self.id,
            "name" : self.name,
            "number" : self.number,
            "email" : self.email
        }

        return j

