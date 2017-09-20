from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from classes import Invoice, InvoiceItem

@view_config(route_name='home')
def home(request):
    return Response("""
        <html lang="en">
            <head></head>
            <body>
                <div>
                    <form action="/invoice" method="POST">
                        <button type="submit">Create</button>
                    </form>
                </div>
            </body>
        </html>
    """)

@view_config(route_name='invoice', request_method='POST')
def invoice(request):
    return HTTPFound(location='/invoice/%s' % Invoice.create())

@view_config(route_name='invoice_item')
def invoice_item(request):
    current_id = request.url.split('/')[-1]

    if(Invoice.find(current_id) is None):
        return HTTPFound(location='/')

    invoice_items = {}
    for item in InvoiceItem.find(current_id):
        invoice_items['units_%s' % item.id] = item.units
        invoice_items['description_%s' % item.id] = item.description
        invoice_items['amount_%s' % item.id] = item.amount

    return Response("""
        <html>
            <head></head>
            <body>
                <div>
                    <form action="/invoice_item/create/%s" method="POST">
                        <label for="units">units</label>
                        <input type="number" id="units" name="units"/>

                        <label for="description">description</label>
                        <input type="text" id="description" name="description"/>

                        <label for="amount">amount</label>
                        <input type="number" id="amount" name="amount"/>

                        <button type="submit">Submit</button>
                    </form>

                    <div>
                        %s
                    </div>
                    <br>
                    <div>
                        <a href="/">create a new invoice</a>
                    </div>
                </div>
            </body>
        </html>
    """ % (current_id, invoice_items))

@view_config(route_name='invoice_item_create', request_method='POST')
def invoice_item_create(request):

    invoice_id = request.url.split('/')[-1]
    units = request.params['units']
    description = request.params['description']
    amount = request.params['amount']

    invoice_item = InvoiceItem.create(invoice_id,units,description,amount)

    return HTTPFound(location='/invoice/%s' % invoice_id)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('invoice', '/invoice')
        config.add_route('invoice_item','/invoice/{id}')
        config.add_route('invoice_item_create', '/invoice_item/create/{id}')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('216.98.139.16', 80, app)
    server.serve_forever()
