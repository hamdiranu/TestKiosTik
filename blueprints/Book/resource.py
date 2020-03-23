from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *
from .model import Books
from blueprints import db,app, admin_required

bp_book = Blueprint('book', __name__)
api = Api(bp_book)

################################################
#              USING RESTFUL-API               #  
################################################

class BookResource(Resource):

    def __init__(self):
        pass

    def get(self, id):
        qry = Books.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Books.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('buku', location = 'json', required = True)
        parser.add_argument('penulis', location = 'json', required = True)
        parser.add_argument('kategori', location = 'json', required = True)
        args = parser.parse_args()

        book = Books(args['buku'], args['penulis'], args['kategori'])
        db.session.add(book)
        db.session.commit()

        app.logger.debug('DEBUG : %s', book)

        return marshal(book, Books.response_fields), 200, {'Content-Type' : 'application/json' }
    
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('buku', location = 'json', required = True)
        parser.add_argument('penulis', location = 'json', required = True)
        parser.add_argument('kategori', location = 'json', required = True)
        args = parser.parse_args()

        qry = Books.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.buku = args['buku']
        qry.penulis = args['penulis']
        qry.kategori = args['kategori']
        db.session.commit()

        return marshal(qry, Books.response_fields), 200, {'Content-Type' : 'application/json' }

    def delete(self,id):
        qry = Books.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        # Soft Delete
        qry.deleted = True
        db.session.commit()
        return {'status':'Deleted'}, 200

    def patch(self):
        return 'Not yet implement', 501

class BookList(Resource):

    def __init__(self):
        pass

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('buku', location = 'args')
        parser.add_argument('penulis', location = 'args')
        parser.add_argument('kategori', location = 'args')
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Books.query

        if args['buku'] is not None:
            qry = Books.query.filter(Books.buku.like("%"+args['buku']+"%"))
        if args['penulis'] is not None:
            qry = Books.query.filter(Books.penulis.like("%"+args['penulis']+"%"))
        if args['kategori'] is not None:
            qry = Books.query.filter(Books.kategori.like("%"+args['kategori']+"%"))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Books.response_fields))
        return rows, 200

api.add_resource(BookResource, '', '/<id>')
api.add_resource(BookList, '', '/list')