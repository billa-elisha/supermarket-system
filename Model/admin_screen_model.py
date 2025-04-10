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
            return []
        finally:
            db.close()

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
            db.close()
        except Exception as e:
            print(e)

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
            return None

    def updateProduct(self, pId, pCode, pName, pCprice, pSprice, pQt):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(
                f"update products SET product_bar_code='{pCode}',product_name='{pName}',product_cost_price={pCprice},product_selling_price={pSprice},product_quantity={pQt} where product_id={pId};"
            )
            db.commit()
            db.close()
        except Exception as e:
            print(e)
            pass

    def deleteProduct(self, productToDelete):
        try:
            db = self.database
            cur = db.cursor()

            cur.execute(f"""delete from products where product_id={productToDelete};""")
            db.commit()
            db.close()
        except Exception as e:
            # if the product deleted is not found

            return "No"
