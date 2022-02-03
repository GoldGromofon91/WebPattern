from jinja2 import Template, Environment, FileSystemLoader


def render_template(template_name, folder='templates', **kwargs):
    # Окружение для базовых шаблонов
    jinja_env = Environment()
    # Размещение наших шаблонов
    jinja_env.loader = FileSystemLoader(folder)
    # Получаем наш шаблон из каталога
    template = jinja_env.get_template(template_name)
    return template.render(**kwargs)
