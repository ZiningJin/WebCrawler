from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bci_uniqueid_tbl(db.Model):
    __tablename__ = 'bci_uniqueid_tbl'
    __table_args__ = {'schema': 'leads'}
    projectid = db.Column('projectid', db.Integer, primary_key=True, nullable=True)
    country = db.Column('country', db.String(255), nullable=True)