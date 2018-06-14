from app import db
from sqlalchemy.event import listen
from sqlalchemy import event, DDL
from sqlalchemy.sql import expression

topping_burger_join_table = db.Table(
    'topping_burger_join_table',
    db.Column('burger_id', db.Integer, db.ForeignKey('burgers.id')),
    db.Column('topping_id', db.Integer, db.ForeignKey('toppings.id'))
)

class Burger(db.Model):

    __tablename__ = 'burgers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    has_bun = db.Column(db.Boolean(create_constraint=True), server_default=expression.true())
    has_patty = db.Column(db.Boolean(create_constraint=True), server_default=expression.true())

    toppings = db.relationship('Topping', secondary=topping_burger_join_table)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Burger.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Burger: {}>".format(self.name)

class Topping(db.Model):
    """This class represents the toppings table."""

    __tablename__ = 'toppings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Topping: {}>".format(self.name)
