from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from Model.database import DataBase
import os
import View.screens


class ABMSApp(MDApp):
    KV_DIRS = [os.path.join(os.getcwd(), "View")]
    DEBUG = 1

    def __init__(self, *args, **kwargs):
        super(ABMSApp, self).__init__(*args, **kwargs)
        # self.load_all_kv_files(self.directory)
        # self.screen_manager = MDScreenManager()
        # self.database = DataBase().get_database_connection()

    def build_app(self):
        self.screen_manager = MDScreenManager()
        screens = View.screens.screens
        self.database = DataBase().get_database_connection()

        for i, screen_name in enumerate(screens.keys()):
            model = screens[screen_name]["model"](self.database)
            controller = screens[screen_name]["controller"](model)
            view = controller.get_view()
            view.manager_screen = self.screen_manager
            view.name = screen_name
            self.screen_manager.add_widget(view)
        self.screen_manager.current = "admin screen"
        print(self.screen_manager.screens)
        return self.screen_manager


ABMSApp().run()
