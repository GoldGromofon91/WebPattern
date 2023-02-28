from urllib.parse import unquote

from Framework.jinja_templator import render_template
from Framework.analog_DB import AnalogDB


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', render_template('404.html')


class GetMethodData:
    @staticmethod
    def generate_get_data(data):
        if data and '&' not in data:
            key, val = data.split("=")
            return {key: val}
        if data and '&' in data:
            parametrs = {}
            query_elem = [el for el in data.split('&')]
            for attr in query_elem:
                k, v = attr.split('=')
                parametrs[k] = v
            return parametrs
        return None


class PostMethodData:
    @staticmethod
    def generate_post_data(enviroment):
        post_data = {}
        length_data = enviroment.get('CONTENT_LENGTH')
        data_in_bytes = enviroment['wsgi.input'].read(int(length_data))
        data_in_string = unquote(data_in_bytes.decode("utf8")).replace('+', ' ')
        query_elem = [el for el in data_in_string.split('&')]
        for attr in query_elem:
            k, v = attr.split('=')
            post_data[k] = v
        return post_data


class Core:
    def __init__(self, routes, front_controllers):
        self.routes = routes
        self.FC = front_controllers
        self.request = {
            'METHOD': None,
            'METHOD_GET_QUERY_IN': None,
            'POST_DATA': None
        }

    def __call__(self, environ, response):
        # Берем текущий путь по которому выполнен GET запрос
        current_path = environ["PATH_INFO"]

        # Добавляем '/' в конец пути
        if not current_path.endswith('/'):
            current_path = f'{current_path}/'

        # Добавляем общие ключи SERVER_DATE_TIME,CURRENT_DATE_TIME к объекту request
        for f_controller in self.FC:
            f_controller(self.request)

        # Обрабатывем стандартные методы GET/POST
        # Заполняем словарь
        method = environ.get('REQUEST_METHOD')
        self.request['METHOD'] = method

        if method == "GET" and environ.get('QUERY_STRING'):
            request_param = GetMethodData.generate_get_data(environ.get("QUERY_STRING"))
            self.request['METHOD_GET_QUERY_IN'] = request_param
            AnalogDB.save_in_db(data=self.request)
        if method == "POST" and environ.get('CONTENT_LENGTH'):
            request_param = PostMethodData.generate_post_data(environ)
            self.request['POST_DATA'] = request_param
            AnalogDB.save_in_db(data=self.request)
        # Запускаем соответсвующую вьюху в зависимости от пути
        if current_path in self.routes:
            view = self.routes[current_path]
        else:
            view = PageNotFound404()

        # self.request['new'] = 'TEST_str'
        # AnalogDB.save_in_db(data=self.request)
        status_code, body = view(self.request)
        response(status_code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
