from Controller.admin_screen_controller import AdminScreenController
from Controller.login_screen_controller import LoginScreenContorller
from Model.admin_screen_model import AdminScreenModel
from Model.login_screen_model import LoginScreenModel
from Controller.operator_screen_controller import OperatorScreenController
from Model.operator_screen_model import OperatorScreenModel
from Controller.products_screen_controller import ProductsScreenController
from Model.products_screen_model import ProductsScreenModel

screens = {
    "login screen": {"controller": LoginScreenContorller, "model": LoginScreenModel},
    "operator screen": {
        "controller": OperatorScreenController,
        "model": OperatorScreenModel,
    },
    "admin screen": {"controller": AdminScreenController, "model": AdminScreenModel},
    "products screen": {
        "controller": ProductsScreenController,
        "model": ProductsScreenModel,
    },
}
