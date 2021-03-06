import json

from django.template.loader import render_to_string
from ..exceptions import GraphosException
from ..utils import DEFAULT_HEIGHT, DEFAULT_WIDTH, get_random_string
from ..encoders import GraphosEncoder


class BaseChart(object):

    def __init__(self, data_source, html_id=None,
                 width=None, height=None,
                 options=None, encoder=GraphosEncoder, 
                 *args, **kwargs):
        self.data_source = data_source
        self.html_id = html_id or get_random_string()
        self.height = height or DEFAULT_HEIGHT
        self.width = width or DEFAULT_WIDTH
        self.options = options or {}
        self.header = data_source.get_header()
        self.encoder = encoder
        self.context_data = kwargs

    def get_data(self):
        return self.data_source.get_data()

    def get_data_json(self):
        return json.dumps(self.get_data())

    def get_options(self):
        options = self.options
        if not 'title' in options:
            options['title'] = "Chart"
        return options

    def get_options_json(self):
        return json.dumps(self.get_options(), cls=self.encoder)

    def get_template(self):
        raise GraphosException("Not Implemented")

    def get_html_id(self):
        return self.html_id

    def get_context_data(self):
        return self.context_data

    def as_html(self):
        context = {"chart": self}
        return render_to_string(self.get_template(), context)
