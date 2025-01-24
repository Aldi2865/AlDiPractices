#app/models.py: Визначає моделі бази даних (наприклад, модель AmmunitionStock).

from app import db

class AmmunitionStock(db.Model):
    AmmunitionID = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(64), index=True)
    Quantity = db.Column(db.Integer)
    StorageLocation = db.Column(db.String(120), index=True)
    ExpirationDate = db.Column(db.Date)

    def __repr__(self):
        return '<Ammunition {}>'.format(self.Type)