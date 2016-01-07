
import os
from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ODApp.Routes.Routes import Routes


class ODApp:
    def __init__(self, app):
        self.flask_app = app

        db_login = os.environ['DB_LOGIN'] if ('DB_LOGIN' in os.environ) else 'mysql+pymysql://root@localhost/opendoorlistingsdb'

        # start db connection
        engine = create_engine(db_login)
        self.ODListingsSession = sessionmaker(bind=engine)
        self.listings_session = self.ODListingsSession()

        # routes
        Routes.setup_routes(self)

    def get_listings_session(self):
        if not self.get_listings_session:
            self.listings_session = self.ODListingsSession()

        return self.listings_session

    def start(self):
        self.flask_app.run(debug=False)

    def __exit__(self, exc_type, exc_value, traceback):
        self.listings_session.close()


debug = True
app = Flask(__name__)
ODApp(app)
