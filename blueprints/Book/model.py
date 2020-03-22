from blueprints import db
from flask_restful import fields
import datetime

class Books(db.Model):
    __tablename__= "Book"
    id          = db.Column(db.Integer, primary_key = True, autoincrement = True)
    buku        = db.Column(db.String(255), nullable = False)
    penulis     = db.Column(db.String(255), nullable = False)
    kategori    = db.Column(db.String(255), nullable = False)
    created_at  = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at   = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    deleted     = db.Column(db.Boolean, default = False)

    response_fields = {
        'id'           : fields.Integer,
        'buku'         : fields.Integer,
        'penulis'      : fields.Boolean,
        'kategori'     : fields.Integer,
        'created_at'   : fields.DateTime,
        'updated_at'   : fields.DateTime,
        'deleted'      : fields.Boolean,
    }

    def __init__(self, buku, penulis, kategori):
        self.buku = buku
        self.penulis = penulis
        self.kategori = kategori

    def __repr_(self):
        return '<Book %r>' %self.id