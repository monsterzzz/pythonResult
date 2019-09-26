from engin import db,login

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(120))
    cart = db.relationship('Cart')

class Good(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(64))
    avatar = db.Column(db.String(255))
    description =  db.Column(db.String(64))
    price = db.Column(db.Integer)
    def __repr__(self):
        return "<Good(id='{}', items='{}')>".format(self.id, self.name)

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    good = db.relationship(Good)
    def __repr__(self):
        return "<Cart(id='{}')>".format(self.id)