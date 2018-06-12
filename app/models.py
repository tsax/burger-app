from app import db
from sqlalchemy.sql import expression

class Burger(db.Model):
    """This class represents the burgers table."""

    __tablename__ = 'burgers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    has_bun = db.Column(db.Boolean(create_constraint=True), server_default=expression.true())
    has_patty = db.Column(db.Boolean(create_constraint=True), server_default=expression.true())
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    toppings = db.relationship('Topping', backref='burger', lazy=True)

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
    burger_id = db.Column(db.Integer, db.ForeignKey('burgers.id'), nullable=False)
