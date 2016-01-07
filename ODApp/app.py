
from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Models import Listing
from Routes.Routes import Routes


class ODApp:
    def __init__(self, app):
        self.flask_app = app

        # start db connection
        engine = create_engine('mysql+pymysql://root@localhost/opendoorlistingsdb')
        self.ODListingsSession = sessionmaker(bind=engine)
        self.listings_session = self.ODListingsSession()

        # routes
        Routes.setup_routes(self)

    def get_listings_session(self):
        if not self.get_listings_session:
            self.listings_session = self.ODListingsSession()

        return self.listings_session

    def start():
        self.flask_app.run(debug=debug)

    def __exit__(self, exc_type, exc_value, traceback):
        self.listings_session.close()


debug = True
app = Flask(__name__)
if __name__ == "__main__":
    ODApp(app).start()
