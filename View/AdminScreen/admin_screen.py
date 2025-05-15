from View.base_screen import BaseScreen
from kivy.properties import ObjectProperty


class AdminScreenView(BaseScreen):
    products_data = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.products_data = self.ids.products_data
