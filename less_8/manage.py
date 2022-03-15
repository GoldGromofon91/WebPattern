from wsgiref.simple_server import make_server

from Framework.main import Core
from Framework.setup import MIDDLEWARE
from views import routes

application = Core(routes,MIDDLEWARE)
with make_server('', 8888, application) as server:
    print("Serving on port 8888...")
    server.serve_forever()