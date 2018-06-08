from app import db

class Burger(db.Model):
    """This class represents the burger table."""

    __tablename__ = 'burgers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    has_bun = db.Column(db.Boolean(create_constraint=True))
    has_patty = db.Column(db.Boolean(create_constraint=True))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """Initialize with name."""
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
