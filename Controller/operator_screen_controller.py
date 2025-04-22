from kivy.uix.accordion import ObjectProperty
import View
import View.OperatorScreen
import View.OperatorScreen.operator_screen
from kivy.utils import get_color_from_hex
import decimal as PythonDecimal
import numpy as np

# from tabulate import tabulate
from prettytable import PrettyTable, TableStyle
import pathlib
import win32api
import os
from datetime import datetime


class OperatorScreenController:
    def __init__(self, model):
        self.model = model
        self.view = View.OperatorScreen.operator_screen.OperatorScreenView(
            controller=self, model=self.model
        )
        self.searched_product = []
        # self.product is a dictionary that takes every product you add the cart with it
        # id as the key in the form {5:(5, '34332', 'gary', 5.0, 67.0, 8)}
        self.products_on_the_card = dict()
        self.recently_added_product_id = []  # this is use to help udate the produc_on_the_card when undo is press

    def get_view(self):
        return self.view

    def searchProduct(self, textbox, productNameLable, productPriceLable):
        """
        This function takes the product name or bar code as it value
        to search for the product
        """
        text = str(textbox.text)  # the name or code of product you searched
        #
        productNameLable.text = ""  # making sure the previews product searched details is cleared before processing the new product
        productNameLable.text_color = get_color_from_hex("5C5C5C")
        # indicating an error if you click the search button without entering any product
        if text == "":
            textbox.error = True
            return
        # searching for the product base on the text entered into the search field
        else:
            # this is a list that contains the product searched everytime so we have to clear
            # the previews searche product before we add the new product to it
            self.searched_product.clear()

            # selectProduct is a function in the operator_screen_model.py that takes the
            # the text of the product you search to search it from the database
            product_searched = self.model.selectProduct(text)

            # this condition will turn to true when the product is not in the system
            if str(product_searched) == "None":
                productNameLable.text = "No Product with that name or code"
                productNameLable.text_color = (1, 0, 0, 1)
                return
            # if the product is found in the system this block will be executed
            else:
                # The product search will be a tuple in the form (product_id, product_bar_code,product_name,product_cost_price,product_selling_price,product_quantity)
                # so this condition is use to check the product your search in the system is avalilable or has finished
                if int(product_searched[5]) < 1:
                    productNameLable.text = "Product is out of stock"
                    productNameLable.text_color = (1, 0, 0, 1)
                    return
                else:
                    # if it has not finished we add it to the searched product  lise
                    self.searched_product.append(
                        product_searched
                    )  # ==>[(5, '34332', 'gary', 5.0, 67.0, 8)]
                    try:
                        productNameLable.text = str(self.searched_product[0][2])
                        productPriceLable.text = str(self.searched_product[0][4])
                    except Exception as e:
                        pass

    def clearSearchedProduct(self, productNameLable, productPriceLable):
        self.productNameLable = productNameLable
        self.productPriceLable = productPriceLable
        """
        This function clear the product searched name and price on the user 
        interface.
        it also emptys product-search list variable 

        """
        self.productNameLable.text = ""
        self.productPriceLable.text = ""
        self.searched_product.clear()

    def addToCard(
        self, productNameLable, productPriceLable, recycleview, totalpurchased
    ):
        """It adds and at the same time updates the
        products_on_the_card variable

        """
        namelable = productNameLable
        pricelable = productPriceLable
        # it takes the product searched from the self.searched_product
        try:
            if (
                len(self.searched_product) == 0
            ):  # this turns to true if there is no product in the self.search_product
                return
            else:
                prod = list(self.searched_product[0])
                # updating the product quantity and multplying the
                # amount if it already exist in the cart
                product_to_add_id = str(prod[0])

                if product_to_add_id in (self.products_on_the_card.keys()):
                    # update that Product
                    product_to_update = self.products_on_the_card[
                        f"{product_to_add_id}"
                    ]  # eg ====>[3, '12345', 'techno', 100.0, 899.09, 53, '1', 899.09] where [7] is the main cost of the product and [4] is the newly udated

                    # updating the price
                    product_to_update[4] = (
                        f"{(PythonDecimal.Decimal(f'{product_to_update[4]}') + PythonDecimal.Decimal(f'{product_to_update[7]}'))}"
                    )
                    # updating the quantity
                    product_to_update[6] = f"{int(product_to_update[6]) + int(1)}"
                    updated_product = product_to_update
                    self.products_on_the_card[str(product_to_add_id)] = updated_product
                    recycleview.data = self.display_bill_data(totalpurchased)
                    # adding the id of the updated product back to the  recently added list to help remove incase the undo button is press
                    self.recently_added_product_id.append(str(prod[0]))

                else:
                    # add as a new product
                    "uding initial quantity value as 1"
                    prod.append("1")
                    prod.append(prod[4])  # unit price of the product
                    self.products_on_the_card[f"{prod[0]}"] = prod
                    recycleview.data = self.display_bill_data(totalpurchased)
                    self.recently_added_product_id.append(str(prod[0]))
                self.clearSearchedProduct(namelable, pricelable)
        except Exception as e:
            print(e)
            return None

    def display_bill_data(self, tatalamnt_value):
        data_ = []
        if len(self.products_on_the_card) == 0:
            return data_
        else:
            total_amount = []
            for id_ in self.products_on_the_card.keys():
                item = self.products_on_the_card[f"{id_}"][2]
                amount = self.products_on_the_card[f"{id_}"][4]
                qt = self.products_on_the_card[f"{id_}"][6]
                unitprice = self.products_on_the_card[f"{id_}"][7]
                data_.append({"text": f"{item}"})
                data_.append({"text": f"{unitprice}"})
                data_.append({"text": f"{qt}"})
                data_.append({"text": f"{amount}"})
                total_amount.append(str(amount))
            total = PythonDecimal.Decimal("0.00")
            print(total_amount)
            for price in total_amount:
                total += PythonDecimal.Decimal(f"{price}")
            tatalamnt_value.text = str(total)

            return data_

    def undoButton(self, recycleview):
        # if the last product in the product to add to card chain
        # quantity value is more than one, reduce it and subtract the unit price from the amount
        # else we remove the entire product
        try:
            key_of_the_last_product = str(self.recently_added_product_id[-1])
            product_to_undo = self.products_on_the_card[key_of_the_last_product]
            if int(product_to_undo[6]) > 1:
                product_to_undo[6] = f"{int(product_to_undo[6]) - int(1)}"
                product_to_undo[4] = (
                    f"{(PythonDecimal.Decimal(f'{product_to_undo[4]}') - PythonDecimal.Decimal(f'{product_to_undo[7]}'))}"
                )
                self.products_on_the_card[key_of_the_last_product] = product_to_undo
                # getting acess to the total cost lable so that i can update the price
                self.totalAmount = self.view.ids["totalpurchased"]

                recycleview.data = self.display_bill_data(self.totalAmount)

            else:
                # delete the product
                product_to_undo[4] = (
                    f"{(PythonDecimal.Decimal(f'{product_to_undo[4]}') - PythonDecimal.Decimal(f'{product_to_undo[7]}'))}"
                )
                self.products_on_the_card[key_of_the_last_product] = product_to_undo
                new_list = []
                for i in self.recently_added_product_id:
                    if i != key_of_the_last_product:
                        new_list.append(i)

                self.recently_added_product_id = new_list

                # getting acess to the total cost lable so that i can update the price
                self.totalAmount = self.view.ids["totalpurchased"]
                recycleview.data = self.display_bill_data(self.totalAmount)
                del self.products_on_the_card[key_of_the_last_product]
                recycleview.data = self.display_bill_data(self.totalAmount)

        except IndexError as e:
            self.totalAmount.text = str("0.00")
            print(e)
            pass

    def finiliseButton(self, checbox, recycleview, amountsoldtoday, totalpurchased):
        isgeneratebill = checbox.active

        # this is a python table format module to help print the data on a sheet of paper
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.field_names = ["Items", "Rate", "Qt", "Amount"]
        table.align["Items"] = "l"
        table.align["Rate"] = "l"
        table.align["Amount"] = "l"
        table_data = []
        update_product_qt_in_db = []  # contains a list of the id of each product and the qt bought to help me update all the products bought in the database
        if isgeneratebill:
            for purchased_prod_id in self.products_on_the_card.keys():
                # arranging the product data into the table for printing
                table_data.append(
                    [
                        self.products_on_the_card[purchased_prod_id][2],
                        self.products_on_the_card[purchased_prod_id][7],
                        self.products_on_the_card[purchased_prod_id][6],
                        self.products_on_the_card[purchased_prod_id][4],
                    ]
                )
                #
                update_product_qt_in_db.append(
                    [
                        self.products_on_the_card[purchased_prod_id][0],
                        self.products_on_the_card[purchased_prod_id][6],
                        self.products_on_the_card[purchased_prod_id][2],
                        self.products_on_the_card[purchased_prod_id][4],
                        self.products_on_the_card[purchased_prod_id][3],
                        self.products_on_the_card[purchased_prod_id][
                            1
                        ],  # --------------
                    ]
                )
            table.add_rows(table_data)
            table.add_row(["", "", "Totol:", f"{totalpurchased.text}"])
            file_path = str(
                pathlib.Path(__file__).parent.parent.absolute().joinpath("bill.txt")
            )
            # removing previews bill
            try:
                os.remove(file_path)
            except Exception as e:
                pass
            # if the products_on_the_card is empty
            if len(self.products_on_the_card) == 0:
                return
            else:
                # writing the reciept or bill to a .txt file
                with open("bill.txt", "w+") as file:
                    data = (
                        str(table.get_string())
                        .encode("ascii", "ignore")
                        .decode("ascii")
                    )
                    # compandy details

                    c_details = f"""
 Name : {"WorldTech"}
 Contact : {"045456566"}
 Location : {"Bolgatanga"}
{data}
    """
                    file.write(c_details)
                    file.close()
                # printing bill
                win32api.ShellExecute(0, "print", file_path, None, ".", 0)

                # clearing the products that the person bought after genering bill
                self.products_on_the_card.clear()
                recycleview.refresh_from_data()
                recycleview.data = ""

                # updating the product quantity in the database
                for pr in update_product_qt_in_db:
                    try:
                        product_id = pr[0]
                        qt_purcharesed = pr[1]
                        self.model.updateProduct(product_id, qt_purcharesed)
                        print(pr)
                        # adding each sold product to the sales table
                        pname = str(pr[2])
                        qtsold = int(pr[1])
                        amntsold = float(pr[3])

                        profit = str(
                            PythonDecimal.Decimal(f"{amntsold}")
                            - (qtsold * PythonDecimal.Decimal(f"{float(pr[4])}"))
                        )
                        product_code = str(pr[5])
                        soldDate = datetime.now()
                        date = soldDate.strftime("%d %b %Y")
                        month = soldDate.strftime("%b %Y")
                        year = soldDate.strftime("%Y")

                        self.model.insertInToSalesTable(
                            product_code,
                            pname,
                            qtsold,
                            amntsold,
                            profit,
                            date,
                            month,
                            year,
                        )
                    except Exception as e:
                        print(e)
                        pass
                update_product_qt_in_db.clear()
        else:
            for purchased_prod in self.products_on_the_card.keys():
                update_product_qt_in_db.append(
                    [
                        self.products_on_the_card[purchased_prod][0],
                        self.products_on_the_card[purchased_prod][6],
                    ]
                )
            self.products_on_the_card.clear()
            recycleview.refresh_from_data()
            recycleview.data = ""
            # udating the product quantity in the database
            for pr in update_product_qt_in_db:
                try:
                    product_id = pr[0]
                    qt_purcharesed = pr[1]
                    self.model.updateProduct(product_id, qt_purcharesed)

                    # adding each sold product to the sales table
                    pname = str(pr[2])
                    qtsold = int(pr[1])
                    amntsold = float(pr[3])

                    profit = str(
                        PythonDecimal.Decimal(f"{amntsold}")
                        - (qtsold * PythonDecimal.Decimal(f"{float(pr[4])}"))
                    )

                    soldDate = datetime.now()
                    date = soldDate.strftime("%d %b %Y")
                    month = soldDate.strftime("%b %Y")
                    year = soldDate.strftime("%Y")
                    # print(month, year)

                    self.model.insertInToSalesTable(
                        pname, qtsold, amntsold, profit, date, month, year
                    )
                except Exception as e:
                    print(e)
                    pass
            update_product_qt_in_db.clear()
        amountsoldtoday.text = str(
            np.float64(str(self.model.amountSoldOnEachDay())).round(decimals=2)
        )

    # ==========================================================================
