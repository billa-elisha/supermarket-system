# from Model.database import DataBase


class LoginScreenModel:
    def __init__(self, database):
        self.database = database

    def select_user_data(self, userName, userPassword):
        try:
            db = self.database
            cur = db.cursor()
            cur.execute(
                f"SELECT user_name,user_password from user where user_name='{userName}' AND user_password='{userPassword}';"
            )
            user_data = cur.fetchone()
            return user_data
        except Exception as e:
            pass

        # self.creat_user_table()

    # def validate_user_login_cridentials(self):
    #     return self.database.get_database_connection()

    # def creat_user_table(self):
    #     conn = self.database.get_database_connection()

    #     cur = conn.cursor()
    #     cur.execute(
    #         """CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT);"""
    #     )
