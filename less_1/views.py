from Framework.jinja_templator import render_template


class Index:
    def __call__(self, request):
        return '200 OK', render_template('index.html',
                                         data={
                                             'server_time': request.get('SERVER_DATE_TIME', None),
                                             'moscow_time': request.get('CURRENT_DATE_TIME', None)
                                         })


class Items:
    def __call__(self, request):
        return '200 OK', render_template('items.html',
                                         data={'moscow_time': request.get('CURRENT_DATE_TIME', None)})


class Contacts:
    def __call__(self, request):
        return '200 OK', render_template('contact.html')
