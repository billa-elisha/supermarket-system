import View
import View.OperatorScreen
import View.OperatorScreen.operator_screen
from kivy.utils import get_color_from_hex
import decimal as PythonDecimal

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
        self.products_on_the_card = dict()
        self.recently_added_product_id = []  # this is use to help udate the produc_on_the_card when undo is press

    def get_view(self):
        return self.view

    def searchProduct(self, textbox, productNameLable, productPriceLable):
        """
        This function takes the product name or bar code as it value
        to search for the product
        """
        text = str(textbox.text)
        productNameLable.text = ""
        productNameLable.text_color = get_color_from_hex("5C5C5C")
        if text == "":
            textbox.error = True
            return
        else:
            self.searched_product.clear()
            product_searched = self.model.selectProduct(text)
            if str(product_searched) == "None":
                productNameLable.text = "No Product with that name or code"
                productNameLable.text_color = (1, 0, 0, 1)
                return
            else:
                if int(product_searched[5]) < 1:
                    productNameLable.text = "Product is out of stock"
                    productNameLable.text_color = (1, 0, 0, 1)
                    return
                else:
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
            if len(self.searched_product) == 0:
                return
            else:
                prod = list(self.searched_product[0])
                # apdating the product quantity and multplying the
                # amount if it already exist
                product_to_add_id = str(prod[0])
                if product_to_add_id in (self.products_on_the_card.keys()):
                    # update that Product
                    product_to_update = self.products_on_the_card[
                        f"{product_to_add_id}"
                    ]
                    # updating the price
                    product_to_update[4] = (
                        f"{(PythonDecimal.Decimal(f'{product_to_update[4]}') + PythonDecimal.Decimal(f'{product_to_update[7]}'))}"
                    )
                    product_to_update[6] = f"{int(product_to_update[6]) + int(1)}"
                    updated_product = product_to_update
                    self.products_on_the_card[str(product_to_add_id)] = updated_product
                    recycleview.data = self.display_bill_data(totalpurchased)
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
            pass

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
            total = PythonDecimal.Decimal("0.0")
            for price in total_amount:
                total += PythonDecimal.Decimal(f"{price}")
            tatalamnt_value.text = str(total)
            # tatalamnt_value.text = str(sum(PythonDecimal.Decimal(f"{total_amount}")))

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
                recycleview.data = self.display_bill_data()

            else:
                # delete the product
                del self.products_on_the_card[key_of_the_last_product]
                new_list = []
                for i in self.recently_added_product_id:
                    if i != key_of_the_last_product:
                        new_list.append(i)

                self.recently_added_product_id = new_list
                recycleview.data = self.display_bill_data()

        except IndexError as e:
            pass

    def finiliseButton(self, checbox, recycleview, amountsoldtoday, totalpurchased):
        isgeneratebill = checbox.active

        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.field_names = ["Items", "Rate", "Qt", "Amount"]
        table.align["Items"] = "l"
        table.align["Rate"] = "l"
        table.align["Amount"] = "l"
        table_data = []
        update_product_qt_in_db = []  # contains a list of the id of each product and the qt bought
        if isgeneratebill:
            for purchased_prod in self.products_on_the_card.keys():
                table_data.append(
                    [
                        self.products_on_the_card[purchased_prod][2],
                        self.products_on_the_card[purchased_prod][7],
                        self.products_on_the_card[purchased_prod][6],
                        self.products_on_the_card[purchased_prod][4],
                    ]
                )
                update_product_qt_in_db.append(
                    [
                        self.products_on_the_card[purchased_prod][0],
                        self.products_on_the_card[purchased_prod][6],
                        self.products_on_the_card[purchased_prod][2],
                        self.products_on_the_card[purchased_prod][4],
                        self.products_on_the_card[purchased_prod][3],
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
            except:
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

                        self.model.insertInToSalesTable(
                            pname, qtsold, amntsold, profit, date, month
                        )
                    except Exception as e:
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

                    self.model.insertInToSalesTable(
                        pname, qtsold, amntsold, profit, date, month
                    )
                except:
                    pass
            update_product_qt_in_db.clear()
        amountsoldtoday.text = str(self.model.amountSoldOnEachDay())

    # ==========================================================================
