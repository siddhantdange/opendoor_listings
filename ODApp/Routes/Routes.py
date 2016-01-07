
from ODApp.Controllers.Listings import Listings

GET_ROUTES = [
    ('/listings', Listings.get_listings),
]

class Routes():
  @staticmethod
  def setup_routes(od_app):
    for setting in GET_ROUTES:
      url, func = setting
      def wrapper():
          return func(od_app)
      Router(od_app).get(url=url, func=wrapper)

class Router():
  def __init__(self, od_app):
    self.od_app = od_app

  def get(self, url, func):
    if self.od_app:
      self.od_app.flask_app.route(url, methods=['GET'])(func)
