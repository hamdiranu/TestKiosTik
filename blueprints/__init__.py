import json, os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_restful import Resource, Api
import json, logging
from logging.handlers import RotatingFileHandler
import datetime
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# u_name = os.environ["THIS_U_NAME"]
# password = os.environ["THIS_PASSWORD"]
# endpoint = os.environ["THIS_ENDPOINT"]
# db_test = os.environ["THIS_DB_TEST"]
# db_dev = os.environ["THIS_DB_DEV"]

app.config['APP_DEBUG'] = True

############################
#           JWT            #
############################

app.config['JWT_SECRET_KEY'] = 'SFsieaaabjsdalkjdi32jdijd32657j'
app.config['JWT_ACCES_TOKEN_EXPIRES'] = datetime.timedelta(days = 1)

jwt = JWTManager(app)

###########################
#         Database        #
###########################

try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hamdiranu:8hamdiranu9@0.0.0.0:3306/db_test_kiostiktest'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hamdiranu:8hamdiranu9@0.0.0.0:3306/db_kiostiktest'

except Exception as e:
    raise e    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['isadmin']:
            return {'status': 'FORBIDDEN', 'message': 'admin Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

db = SQLAlchemy(app)
mirate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


######################
#  Import Blueprint  #
######################

@app.after_request
def after_request(response):
    try :
        requestData = request.get_json()
    except Exception as e :
        requestData = request.args.to_dict()
    if response.status_code == 200 :
        app.logger.info("REQUEST_LOG\t%s",json.dumps({
            'status_code':response.status_code,
            'method':request.method,
            'code':response.status,
            'uri':request.full_path,
            'request': request.args.to_dict(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )

    elif response.status_code == 501 :
        app.logger.error("REQUEST_LOG\t%s",json.dumps({
            'status_code':response.status_code,
            'method':request.method,
            'code':response.status,
            'uri':request.full_path,
            'request': request.args.to_dict(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )

    else:
        app.logger.warning("REQUEST_LOG\t%s",json.dumps({
            'status_code':response.status_code,
            'method':request.method,
            'code':response.status,
            'uri':request.full_path,
            'request': request.args.to_dict(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response

from blueprints.Book.resource import bp_book

app.register_blueprint(bp_user, url_prefix = '/book')

db.create_all()
