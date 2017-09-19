from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home')
def home(request):
    return Response
    ("""
        <form action="/test" method="post">
            <input id="invoice" name="invoice" value=""/><br>
            <input type="submit" value="submit">
        </form>
    """)

@view_config(route_name='test', request_method='POST')
def test(request):
    return Response('%s' % request.params['invoice'])

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('test', '/test')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('216.98.139.16', 8080, app)
    server.serve_forever()
