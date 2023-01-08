from cassa import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    matricola = db.Column(db.String(length=6), nullable=False, unique=True)
    password = db.Column(db.String(length=6), nullable=False)

    def check_password_correction(self, attempted_password):
        return self.password == attempted_password


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)

    @property
    def __repr__(self):
        return f'Item {self.name}'


class Receipt(db.Model):
    id = db.Column(db.Integer(), primary_key=True)


class ReceiptsItems(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    receipt = db.Column(db.Integer(), db.ForeignKey('receipt.id'))
    item = db.Column(db.Integer(), db.ForeignKey('item.id'))
