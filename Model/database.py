import sqlite3


class DataBase:
    def __init__(self):
        self.create_products_table()
        self.create_sales_table()
        self.create_user_table()
        self.create_company_details_table()
        # self.creatingDefaulCompanyDetails()
        # self.creatingDefautLogedInuser()

    def get_database_connection(self):
        return sqlite3.connect("SDBase.db")

    def create_user_table(self):
        db = self.get_database_connection()
        cursor = db.cursor()
        query = """CREATE TABLE IF NOT EXISTS user(
                 user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_first_name TEXT NOT NULL,
                 user_last_name TEXT NOT NULL,
                 user_password TEXT NOT NULL,
                 user_designation TEXT NOT NULL,
                 user_contact INTEGER NOT NULL);"""
        cursor.execute(query)

    def create_products_table(self):
        """This function is use to create the users table
        and it is called in the init method
        """
        db = self.get_database_connection()
        cursor = db.cursor()
        quary = """CREATE TABLE IF NOT EXISTS products(
                 product_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 product_bar_code text NOT NULL, 
                 product_name text NOT NULL, 
                 product_cost_price real NOT NULL,
                 product_selling_price real NOT NULL,
                 product_quantity integer NOT NULL
                );"""
        cursor.execute(quary)

    def create_sales_table(self):
        """This function is use to create the sales table
        and it is called in the init method
        """
        try:
            db = self.get_database_connection()
            cursor = db.cursor()
            quary = """CREATE TABLE IF NOT EXISTS sales(
                    sales_id INTEGER PRIMARY KEY,
                    product_code text NOT NULL,
                    product_name text NOT NULL,
                    quantity_sold INTEGER NOT NULL,
                    amount_sold REAL NOT NULL,
                    profit_made REAL NOT NULL,
                    date TEXT NOT NULL,
                    month TEXT NOT NULL,
                    year TEXT NOT NULL
                    );"""
            cursor.execute(quary)

        except Exception as e:
            pass

    def create_company_details_table(self):
        """This function is use to create the create_company_details table
        and it is called in the init method
        """
        try:
            db = self.get_database_connection()
            cursor = db.cursor()
            quary = """CREATE TABLE IF NOT EXISTS company_details(
                    company_id INTEGER PRIMARY KEY,
                    company_name text NOT NULL,
                    company_location text NOT NULL,
                    company_contact text NOT NULL
                    );"""
            cursor.execute(quary)

        except Exception as e:
            print(e)
            pass

    def creatingDefautLogedInuser(self):
        try:
            db = self.get_database_connection()
            cursor = db.cursor()

            q = """insert into products values('product_id','1234','sumsong',80.6,90.0,78.0);"""
            cursor.execute(q)
            db.commit()

        except Exception as e:
            print(e)
            pass

    def creatingDefaulCompanyDetails(self):
        try:
            db = self.get_database_connection()
            cursor = db.cursor()

            q = """insert into company_details(company_name,company_location,company_contact) values('Enter_your_company_name','Enter_your_company_location','Enter_your_company_contact_number');"""
            cursor.execute(q)
            db.commit()

        except Exception as e:
            print(e)
            pass


# DataBase()
# def logedInUsersTable(self):
#     """This function is use to create the users table
#     and it is called in the init method
#     """
#     mydb = sqlite3.connect(dbname)
#     mycursor = mydb.cursor()
#     quary1 = ('''CREATE TABLE IF NOT EXISTS UserLogedIn(
#              luser_id INTEGER PRIMARY KEY,
#              name text NOT NULL,
#              id text);''')
#     mycursor.execute(quary1)
#     mydb.close()

# def companyDetailsTable(self):
#     """This function is use to create the company details table
#     and it is called in the init method

#     """
#     try:
#         mydb = sqlite3.connect(dbname)
#         mycursor = mydb.cursor()
#         quary = ('''CREATE TABLE IF NOT EXISTS company(
#                 company_id INTEGER PRIMARY KEY,
#                 company_name text,
#                 company_tell text,
#                 company_location text);''')
#         mycursor.execute(quary)
#         mydb.commit()
#         mydb.close()

#         mydb =self.mydb
#         cur = mydb.cursor()
#         iscompanyempty = 'select company_name from company'
#         cur.execute(iscompanyempty)
#         names=cur.fetchall()
#         try:
#             length=len([i for i in names[0]])
#         except:
#             self.creatingDefautCompanyDetails()

#         mydb.close()
#         # if length <=0:
#         #     self.creatingDefautCompanyDetails()
#     except Exception as e:
#         pass

# def deletingFoldersDates(self):
#     """This function is use to create the date table
#     and it is called in the init method
#     """
#     try:
#         mydb = sqlite3.connect(dbname)
#         mycursor = mydb.cursor()
#         quary = ('''CREATE TABLE IF NOT EXISTS recordFilesDeletedDays(
#                 date_id INTEGER PRIMARY KEY,
#                 date TEXT NOT NULL
#                 );''')
#         mycursor.execute(quary)
#         mydb.close()
#     except:
#         pass

# def creatingDefautCompanyDetails(self):
#     try:
#         mydb = sqlite3.connect(dbname)
#         mycursor = mydb.cursor()
#         company = 'insert into company (company_name,company_tell,company_location) values("Enter Company Name","9999999","Enter Company Location")'
#         mycursor.execute(company)
#         mydb.commit()
#         mydb.close()
#     except:
#         pass
