from datetime import datetime
from log.logs import Logs


class OperatorScreenModel:
    def __init__(self, database):
        self.database = database

    def fetchSearchedProduct(self, pName, pCode):
        """search by product name or product bar code"""
        pName = pName
        pCode = pCode
        try:
            db = self.database
            cur = db.cursor()

            if pName == "" and pCode == "":
                return
            elif pName != "" and pCode == "":
                # search by name
                cur.execute(f"SELECT * from products where product_name='{pName}';")
                product = cur.fetchone()
                return product
            elif pName == "" and pCode != "":
                # search by code
                cur.execute(
                    f"SELECT * from products where product_bar_code ='{pCode}';"
                )
                product = cur.fetchone()
                return product
        except Exception as e:
            Logs().logException(str(e))

    def selectProduct(self, product_dentity):
        # This is the structure of the product table
        #      product_id INTEGER PRIMARY KEY,
        #      product_bar_code text NOT NULL,
        #      product_name text NOT NULL,
        #      product_cost_price real NOT NULL,
        #      product_selling_price real NOT NULL,
        #      product_quantity INTEGER NOT NULL
        """
        This function returns the product that is search for by
        the user.
        The product identity could be
        ** the name or
        ** the barcode
        It either returns the product in the form (5, '34332', 'gary', 5.0, 67.0, 8) or
        'None'
        """
        self.product_dentity = product_dentity
        try:
            db = self.database
            cursor = db.cursor()
            cursor.execute(
                f"SELECT * from products where product_name='{self.product_dentity}' or product_bar_code ='{self.product_dentity}' ;"
            )
            product = cursor.fetchone()
            return product
        except Exception as e:
            Logs().logException(str(e))
            return None

    def updateProduct(self, id, qt):
        # This is the structure of the product table
        #      product_id INTEGER PRIMARY KEY,
        #      product_bar_code text NOT NULL,
        #      product_name text NOT NULL,
        #      product_cost_price real NOT NULL,
        #      product_selling_price real NOT NULL,
        #      product_quantity INTEGER NOT NULL
        """
        is use to update the product qt
        """
        product_id = str(id)

        try:
            db = self.database
            cursor = db.cursor()
            cursor.execute(
                f"select product_quantity from products where product_id={product_id};"
            )
            initial_qt = cursor.fetchone()[0]
            product_qt = int(initial_qt) - int(qt)
            # updating
            cursor.execute(
                f"update products SET product_quantity={product_qt} where product_id='{product_id}';"
            )
            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def insertInToSalesTable(
        self,
        product_code: str,
        name: str,
        qt_sold: int,
        amnt_sold: float,
        profit: float,
        date: str,
        month: str,
        year: str,
    ):
        # This is the structure of the product table
        # sales_id INTEGER PRIMARY KEY,
        # product_code text NOT NULL,
        # product_name text NOT NULL,
        # quantity_sold INTEGER NOT NULL,
        # amount_sold REAL NOT NULL,
        # profit_made REAL NOT NULL,
        # date TEXT NOT NULL,
        # month TEXT NOT NULL

        """
        adds product purchase to the sales table
        """

        try:
            db = self.database
            cursor = db.cursor()
            cursor.execute(
                f"insert into sales (product_code,product_name,quantity_sold,amount_sold,profit_made,date,month,year) values('{product_code}','{name}',{qt_sold},{amnt_sold},{profit},'{date}','{month}','{year}');"
            )

            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def amountSoldOnEachDay(self):
        # This is the structure of the product table
        # sales_id INTEGER PRIMARY KEY,
        # product_name text NOT NULL,
        # quantity_sold INTEGER NOT NULL,
        # amount_sold REAL NOT NULL,
        # profit_made REAL NOT NULL,
        # date TEXT NOT NULL,
        # month TEXT NOT NULL

        """
        returns the sum of products sold base on the day
        """
        Date_ = datetime.now()
        todaysDate = Date_.strftime("%d %b %Y")

        try:
            db = self.database
            cursor = db.cursor()
            cursor.execute(
                f"select SUM(amount_sold) from sales where date='{todaysDate}';"
            )
            total = cursor.fetchone()[0]
            if total == None:
                return 0.00
            else:
                return total

        except Exception as e:
            Logs().logException(str(e))

    def select_user_designation(self, userPassword, uName):
        try:
            db = self.database
            cur = db.cursor()
            cur.execute(
                f"SELECT user_designation from user where user_password='{userPassword}' AND user_first_name='{uName}';"
            )
            user_disig = cur.fetchone()
            return user_disig
        except Exception as e:
            return ("None",)

    def returnCompanyDetails(self):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute("select * from company_details;")
            details = cur.fetchall()
            return details

        except Exception as e:
            Logs().logException(str(e))

    def selectAllOutOfStockProducts(self):
        try:
            db = self.database
            cur = db.cursor()
            # displaying the selected product
            # date TEXT NOT NULL,
            # month TEXT NOT NULL,
            # year TEXT NOT NULL

            cur.execute("SELECT * from products where product_quantity=0;")
            outOfStock = cur.fetchall()
            return outOfStock
        except Exception as e:
            Logs().logException(str(e))
            return []
