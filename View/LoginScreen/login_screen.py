from kivy.properties import ObjectProperty
from View.base_screen import BaseScreen


class LoginScreenView(BaseScreen):
    """
    The login screen of the app
    attr:
        1. self.model: Model.login_model.LoginScreenModel
            (to help you intereact with the database)
        2. self.controller : Controller.login_controller.LoginScreenController
            (where the logic of the login screen is found)
    """

    user_name = ObjectProperty()
    user_password = ObjectProperty()
    user_error_ms = ObjectProperty()
    user_name = ObjectProperty()
    user_password = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def sign_in_button_clicked(self):
        userName = self.user_name.text
        userPassword = self.user_password.text
        error_ms = self.user_error_ms
        user_password = self.user_password
        user_name = self.user_name
        self.controller.validate_user(
            userName, userPassword, error_ms, user_password, user_name
        )

    def show_hide_password_button_clicked(self, value, show_pass, user_password):
        value = value
        show_pass = show_pass
        user_password = user_password
        self.controller.show_hide_password(value, show_pass, user_password)
