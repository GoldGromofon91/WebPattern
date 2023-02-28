from Framework.jinja_templator import render_template


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', render_template('404.html')


class Application:
    def __init__(self, routes, front_controllers):
        self.routes = routes
        self.FC = front_controllers

    def __call__(self, environ, response):
        # print(environ.keys())
        # Берем текущий путь по которому выполнен GET запрос
        current_path = environ["PATH_INFO"]

        # Добавляем '/' в конец пути
        if not current_path.endswith('/'):
            current_path = f'{current_path}/'

        # Запускаем соответсвующую вьюху в зависимости от пути
        if current_path in self.routes:
            view = self.routes[current_path]
        else:
            view = PageNotFound404()

        # Добавляем общие ключи SERVER_DATE_TIME,CURRENT_DATE_TIME к объекту request
        request = {}
        for f_controller in self.FC:
            f_controller(request)

        # print(request.keys())
        status_code, body = view(request)
        response(status_code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
