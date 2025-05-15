import View
import View.LoginScreen
import View.LoginScreen.login_screen
from configparser import ConfigParser
import pathlib
import shutil
from log.logs import Logs


class LoginScreenContorller:
    def __init__(self, model):
        self.model = model
        self.view = View.LoginScreen.login_screen.LoginScreenView(
            controller=self, model=self.model
        )

    def get_view(self):
        return self.view

    def validate_user(self, userName, userPassword, error_ms, user_name, user_password):
        error_ms.text = ""
        try:
            fetched_user_data = self.model.select_user_data(userName, userPassword)
            if fetched_user_data is None:
                "send user details not found"
                error_ms.text = "wrong username/password."
                return
            else:
                "login to the operator window"
                user_name.text = ""
                user_password.text = ""
                self.view.parent.current = "operator screen"
                self.view.parent.transition.direction = "left"

        except Exception as e:
            # there should be a logging system here

            Logs().logException(str(e))

            pass

    def show_hide_password(self, value, show_pass, user_password):
        try:
            if str(value.active) == "True":
                show_pass.icon = "eye"
                user_password.password = False
            else:
                user_password.password = True
                show_pass.icon = "eye-off"
        except Exception as e:
            pass
