from services.db_services.db import db


class TagModel(db.Model):  # inherit from db.model
    __tableName__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    item = db.relationship('ItemModel', back_populates='tags')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }