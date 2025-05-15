# from Model.database import DataBase


class LoginScreenModel:
    def __init__(self, database):
        self.database = database

    def select_user_data(self, userName, userPassword):
        try:
            db = self.database
            cur = db.cursor()
            cur.execute(
                f"SELECT user_first_name,user_password,user_designation from user where user_first_name='{userName}' AND user_password='{userPassword}';"
            )
            user_data = cur.fetchone()
            return user_data
        except Exception as e:
            return None
