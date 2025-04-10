import View
import View.ProductsScreen.products_screen


class ProductsScreenController:
    def __init__(self, model):
        self.model = model
        self.view = View.ProductsScreen.products_screen.ProductsScreenView(
            controller=self, model=self.model
        )

    def get_view(self):
        return self.view
