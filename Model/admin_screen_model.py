from log.logs import Logs


class AdminScreenModel:
    def __init__(self, database):
        self.database = database

    def selectSearchedProduct(self, productIdOrName):
        try:
            db = self.database
            cur = db.cursor()
            # displaying all the products if the search box is empty
            if str(productIdOrName) == "" or (str(productIdOrName).lower()) == "all":
                cur.execute("SELECT * from products;")
                products = cur.fetchall()
                return products
            # displaying the selected product if the name or id of the product is searched
            else:
                cur.execute(
                    f"SELECT * from products where product_name='{productIdOrName}'or product_id='{productIdOrName}'or product_bar_code='{productIdOrName}';"
                )
                product = cur.fetchall()
                return product
        except Exception as e:
            Logs().logException(str(e))
            return []

    def selectSearchedUser(self, userIdOrName):
        try:
            db = self.database
            cur = db.cursor()

            # displaying all the users if the search box is empty
            if str(userIdOrName) == "" or (str(userIdOrName).lower()) == "all":
                cur.execute("SELECT * from user;")
                users = cur.fetchall()
                return users

            # displaying the selected users if the name or id of the user is searched
            else:
                cur.execute(
                    f"SELECT * from user where user_first_name='{userIdOrName}' or user_last_name='{userIdOrName}';"
                )
                user = cur.fetchall()
                return user
        except Exception as e:
            Logs().logException(str(e))
            return []

    def selectAllProduct(self):
        """This function selects all the products in the database"""
        try:
            db = self.database
            cur = db.cursor()
            cur.execute("SELECT * from products;")
            allProducts = cur.fetchall()
            if len(allProducts) == 0:
                return ["None"]
            else:
                return allProducts
        except Exception as e:
            Logs().logException(str(e))
            return ["None"]

    def selectAllUsers(self):
        """This function selects all the users in the database"""
        try:
            db = self.database
            cur = db.cursor()
            cur.execute("SELECT * from user;")
            allUsers = cur.fetchall()
            if len(allUsers) == 0:
                return ["None"]
            else:
                return allUsers
        except Exception as e:
            Logs().logException(str(e))
            return ["None"]

    def addProductToDatabase(self, code, name, cprice, sprice, quantity):
        try:
            db = self.database
            cur = db.cursor()
            # converting the data into the correct datatypes befor inserting
            code = str(code)
            name = str(name)
            costprice = float(cprice)
            sellingprice = float(sprice)
            quantity = int(quantity)
            cur.execute(
                f"insert into products(product_bar_code,product_name,product_cost_price,product_selling_price,product_quantity ) values('{code}','{name}',{costprice},{sellingprice},{quantity});"
            )
            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def addUserToDatabase(self, fname, lname, password, designation, contact):
        try:
            db = self.database
            cur = db.cursor()
            # converting the data into the correct datatypes befor inserting
            fname = str(fname)
            lname = str(lname)
            password = str(password)
            designation = str(designation)
            contact = str(contact)

            cur.execute(
                f"insert into user(user_first_name,user_last_name,user_password,user_designation,user_contact) values('{fname}','{lname}','{password}','{designation}','{contact}');"
            )
            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def selectSearchedProductToEdit(self, productIdOrNameOrCode):
        try:
            db = self.database
            cur = db.cursor()
            # displaying all the products if the search box is empty
            if str(productIdOrNameOrCode) == "":
                return
            # displaying the selected product
            else:
                cur.execute(
                    f"SELECT * from products where product_name='{productIdOrNameOrCode}'or product_id='{productIdOrNameOrCode}'or product_bar_code='{productIdOrNameOrCode}';"
                )
                product = cur.fetchone()
                return product
        except Exception as e:
            Logs().logException(str(e))
            return None

    # sales section
    def selectAllSales(self):
        try:
            db = self.database
            cur = db.cursor()
            # displaying the selected product

            cur.execute("SELECT * from sales;")
            sales = cur.fetchall()
            return sales
        except Exception as e:
            Logs().logException(str(e))
            return ["None"]

    def selectSalesByYear(self):
        try:
            db = self.database
            cur = db.cursor()
            # displaying the selected product

            cur.execute("SELECT Distinct(year) from sales;")
            salesByYear = cur.fetchall()
            return salesByYear
        except Exception as e:
            Logs().logException(str(e))
            return ["None"]

    def selectSalesByMonth(self):
        try:
            db = self.database
            cur = db.cursor()
            # displaying the selected product

            cur.execute("SELECT Distinct(month) from sales;")
            salesByMonth = cur.fetchall()
            return salesByMonth
        except Exception as e:
            Logs().logException(str(e))
            return ["None"]

    def selectSalesByDay(self):
        try:
            db = self.database
            cur = db.cursor()
            # displaying the selected product

            cur.execute("SELECT Distinct(date) from sales;")
            salesByDay = cur.fetchall()
            return salesByDay
        except Exception as e:
            Logs().logException(str(e))
            return ["None"]

    def selectSearchedUserToEdit(self, userIdOrfNameOrlName):
        try:
            db = self.database
            cur = db.cursor()
            # displaying all the products if the search box is empty
            if str(userIdOrfNameOrlName) == "":
                return
            # displaying the selected product
            else:
                cur.execute(
                    f"SELECT * from user where user_first_name='{userIdOrfNameOrlName}'or user_id='{userIdOrfNameOrlName}'or user_last_name='{userIdOrfNameOrlName}';"
                )
                user = cur.fetchone()
                return user
        except Exception as e:
            Logs().logException(str(e))
            return None

    def updateProduct(self, pId, pCode, pName, pCprice, pSprice, pQt):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(
                f"update products SET product_bar_code='{pCode}',product_name='{pName}',product_cost_price={pCprice},product_selling_price={pSprice},product_quantity={pQt} where product_id={pId};"
            )
            db.commit()
        except Exception as e:
            Logs().logException(str(e))

    def updateUser(self, uId, fName, lName, password, designation, contact):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(
                f"update user SET user_first_name='{fName}',user_last_name='{lName}',user_password='{password}',user_designation='{designation}',user_contact={contact} where user_id={uId};"
            )
            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def deleteProduct(self, productToDelete):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(
                f"""delete from products where product_id={productToDelete} OR product_bar_code='{productToDelete}';"""
            )
            db.commit()
        except Exception as e:
            # if the product deleted is not found
            Logs().logException(str(e))

            return "No"

    def deleteUser(self, userToDelete):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(f"""delete from user where user_id={userToDelete};""")
            db.commit()
        except Exception as e:
            # if the product deleted is not found
            Logs().logException(str(e))
            return "No"

    def selectSales(self, baseOnWhat):
        try:
            db = self.database
            cur = db.cursor()
            # displaying the selected product
            # date TEXT NOT NULL,
            # month TEXT NOT NULL,
            # year TEXT NOT NULL

            cur.execute(
                f"SELECT * from sales where date='{baseOnWhat}'or month='{baseOnWhat}'or year='{baseOnWhat}';"
            )
            sales = cur.fetchall()
            return sales
        except Exception as e:
            Logs().logException(str(e))
            return ["None"]

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

    def selectAllRuningOutOfStockProducts(self):
        try:
            db = self.database
            cur = db.cursor()
            # displaying the selected product
            # date TEXT NOT NULL,
            # month TEXT NOT NULL,
            # year TEXT NOT NULL

            cur.execute("SELECT * from products where product_quantity<5;")
            outOfStock = cur.fetchall()
            return outOfStock
        except Exception as e:
            Logs().logException(str(e))
            return []

    def updateCompanyName(self, newName):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(
                f"update company_details SET company_name='{newName}' where company_id=1;"
            )
            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def updateCompanyLocation(self, location):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(
                f"update company_details SET company_location='{location}' where company_id=1;"
            )
            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def updateCompanyContact(self, contact):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(
                f"update company_details SET company_contact='{contact}' where company_id=1;"
            )
            db.commit()

        except Exception as e:
            Logs().logException(str(e))

    def returningCompanyDetails(self):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute("select * from company_details;")
            details = cur.fetchall()
            return details

        except Exception as e:
            Logs().logException(str(e))
