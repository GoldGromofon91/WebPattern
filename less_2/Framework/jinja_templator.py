import os.path
from jinja2 import Template


def render_template(template_name, folder='templates', **kwargs):
    file_path = os.path.join(folder, template_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())
    return template.render(**kwargs)
