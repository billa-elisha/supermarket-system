import View
import View.AdminScreen
import View.AdminScreen.admin_screen
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogSupportingText,
)
from kivymd.uix.widget import MDWidget
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldHintText,
    MDTextFieldMaxLengthText,
)

from kivy.utils import get_color_from_hex
import numpy as np
import decimal as decimal
from decimal import Decimal, ROUND_HALF_UP
from log.logs import Logs


class AdminScreenController:
    def __init__(self, model):
        self.model = model
        self.view = View.AdminScreen.admin_screen.AdminScreenView(
            controller=self, model=self.model
        )
        self.displayAllProducts()
        self.displayAllUsers()
        self.labelCompanyDetails()
        self.productsOutOfStockInAdminPage()
        self.productsRuningOutOfStockInAdminPage()

    def get_view(self):
        return self.view

    def goToOperatorPage(self):
        try:
            self.view.parent.current = "operator screen"
            self.view.parent.transition.direction = "right"
        except Exception as e:
            Logs().logException(str(e))

    def confirmToLogoutDialogPopUpBox(self):
        # buttons for the popup field
        try:
            self.NologoutBtn = MDButton(
                MDButtonText(
                    text="No",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                style="text",
            )
            self.yeslogoutBtn = MDButton(
                MDButtonText(
                    text="yes",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                ),
                style="text",
            )
            self.confirmLogoutDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="LOG OUT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Do you relly want to log out?.",
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.yeslogoutBtn,
                    self.NologoutBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.yeslogoutBtn.bind(on_press=self.logOut)
            self.NologoutBtn.bind(on_press=self.confirmLogoutDialogBox.dismiss)
            return self.confirmLogoutDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def logOut(self, *args):
        try:
            self.confirmLogoutDialogBox.dismiss()
            self.view.parent.current = "login screen"
            self.view.parent.transition.direction = "right"
        except Exception as e:
            Logs().logException(str(e))

    def get_parent(self, nav_screen_manager, button):
        try:
            button_name = str(button.text).strip()
            if button_name == "Products":
                nav_screen_manager.current = "products screen"
                return
            if button_name == "Sales":
                nav_screen_manager.current = "sales screen"
                return
            if button_name == "Store details":
                nav_screen_manager.current = "Store details screen"
                return
            if button_name == "Users":
                nav_screen_manager.current = "users screen"
                return
            if button_name == "Out of stock":
                nav_screen_manager.current = "Out of stock screen"
                return
        except Exception as e:
            Logs().logException(str(e))

        # print(v.text)
        # iii.current = "products screen"

    def searchProductByIdOrName(self, adminsearchbox, productIdOrName):
        """This function is called by the search button in the products window
        to display
        1. all the product if the search box is empty or 'all'
        2. display a particular product given its id,name or product bar code

        """
        try:
            selectedProducts = self.model.selectSearchedProduct(
                (str(productIdOrName).lower()).strip()
            )

            # creating an object of the recycle box where all the products will be displayed
            refrencedRecycleview = self.view.products_data

            # giving a message to tell the user that the product that he or she is trying to search those not exist
            if len(selectedProducts) == 0:
                refrencedRecycleview.refresh_from_data()
                refrencedRecycleview.data = [
                    {
                        "text": f"There is no product in the system with name,code or id '{productIdOrName}'"
                    }
                ]

            else:
                """populating the recycle view with the data of
                the searched product"""

                listOfsearchedProducts = []
                for product in selectedProducts:
                    try:
                        productId = {"text": str(product[0])}
                        productCode = {"text": str(product[1])}
                        productName = {"text": str(product[2])}
                        productCprice = {"text": str(product[3])}
                        productSprice = {"text": str(product[4])}
                        productQuantity = {"text": str(product[5])}
                        profit = {
                            "text": f"{np.float64(float(product[4]) - float(product[3])).round(decimals=2)}"
                        }

                        listOfsearchedProducts.append(productId)
                        listOfsearchedProducts.append(productCode)
                        listOfsearchedProducts.append(productName)
                        listOfsearchedProducts.append(productCprice)
                        listOfsearchedProducts.append(productSprice)
                        listOfsearchedProducts.append(productQuantity)
                        listOfsearchedProducts.append(profit)
                    except Exception as e:
                        Logs().logException(str(e))

                # refreshing the recycleview and populating it with data searched
                refrencedRecycleview.refresh_from_data()
                refrencedRecycleview.data = listOfsearchedProducts
            # clearing the searchbox tex
            adminsearchbox.text = ""
        except Exception as e:
            Logs().logException(str(e))

    def displayAllProducts(self):
        try:
            allAvailableProducts = self.model.selectAllProduct()
            # refrencing the recycle view where all the data will be displayed
            recycleviewToDisplayData = self.view.products_data

            dataToDisplay = []
            # display information on the recycle view(tabel containing the list of products) if there are no products in the system
            if allAvailableProducts[0] == "None":
                recycleviewToDisplayData.data = [
                    {"text": "There are no products in the system"}
                ]
            else:
                """ displaying all the available products in the database"""
                for product in allAvailableProducts:
                    try:
                        productId = {"text": str(product[0])}
                        productCode = {"text": str(product[1])}
                        productName = {"text": str(product[2])}
                        productCprice = {"text": str(product[3])}
                        productSprice = {"text": str(product[4])}
                        productQuantity = {"text": str(product[5])}

                        profit = {
                            "text": f"{np.float64(float(product[4]) - float(product[3])).round(decimals=2)}"
                        }

                        dataToDisplay.append(productId)
                        dataToDisplay.append(productCode)
                        dataToDisplay.append(productName)
                        dataToDisplay.append(productCprice)
                        dataToDisplay.append(productSprice)
                        dataToDisplay.append(productQuantity)
                        dataToDisplay.append(profit)
                    except Exception as e:
                        Logs().logException(str(e))

                # populating the table with the selected data
                recycleviewToDisplayData.refresh_from_data()
                recycleviewToDisplayData.data = dataToDisplay
        except Exception as e:
            Logs().logException(str(e))

    # ============================adding product to the database===========================================

    def AddProductDialogPopUpBox(self):
        """This is a popup dialog page that pops up when you click on the
        add button in the products page for you to add the product you want to
        to the database
        """
        # buttons of the popup field
        try:
            self.cancelBtn = MDButton(
                MDButtonText(text="Cancel"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=(1, 0, 0, 1),
            )
            self.addBtn = MDButton(
                MDButtonText(text="Add"),
                MDButtonIcon(
                    icon="plus", theme_icon_color="Custom", icon_color="white"
                ),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("#735FF2"),
            )

            # input fields for the popup box
            self.productCodeTextField = MDTextField(
                MDTextFieldHintText(text="product code", text_color_normal="gray"),
                text="",
                multiline=False,
            )
            self.productNameTextField = MDTextField(
                MDTextFieldHintText(text="product name", text_color_normal="gray"),
                text="",
                multiline=False,
            )
            self.productCpriceTextField = MDTextField(
                MDTextFieldHintText(
                    text="product cost price", text_color_normal="gray"
                ),
                text="",
                multiline=False,
            )
            self.productSpriceTextField = MDTextField(
                MDTextFieldHintText(
                    text="product selling price", text_color_normal="gray"
                ),
                text="",
                multiline=False,
            )
            self.productQuantityTextField = MDTextField(
                MDTextFieldHintText(text="product quantity", text_color_normal="gray"),
                text="",
                multiline=False,
            )

            self.addDialogPopUp = MDDialog(
                MDDialogHeadlineText(
                    text="ADD PRODUCT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text fields for adding the products are kept
                MDDialogContentContainer(
                    self.productCodeTextField,
                    self.productNameTextField,
                    self.productCpriceTextField,
                    self.productSpriceTextField,
                    self.productQuantityTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.addBtn,
                    self.cancelBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.codeText = self.productCodeTextField
            self.nameText = self.productNameTextField
            self.cpriceText = self.productCpriceTextField
            self.spriceText = self.productSpriceTextField
            self.quantityText = self.productQuantityTextField

            self.addBtn.bind(on_press=self.confirmToAddProductDialogPopUpBox)
            self.cancelBtn.bind(on_press=self.addDialogPopUp.dismiss)
            return self.addDialogPopUp
        except Exception as e:
            Logs().logException(str(e))

    def openAddProductDialogPopUpBox(self):
        self.AddProductDialogPopUpBox().open()

    def confirmToAddProductDialogPopUpBox(self, instance, *args):
        # checking to make sure all the fields are not empty
        try:
            if (
                str(self.codeText.text)
                and str(self.nameText.text)
                and str(self.cpriceText.text)
                and str(self.spriceText.text)
                and str(self.quantityText.text)
            ) == "":
                self.productFieldsMustNotBeEmptyPopupBox()
                return

            # buttons for the popup field
            self.NoBtn = MDButton(
                MDButtonText(
                    text="No",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                style="text",
            )
            self.yesBtn = MDButton(
                MDButtonText(
                    text="yes",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                ),
                style="text",
            )
            self.confirmDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ADD PRODUCT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Do you relly want to add this product?.",
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.yesBtn,
                    self.NoBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.yesBtn.bind(on_press=self.addProduct)
            self.NoBtn.bind(on_press=self.confirmDialogBox.dismiss)
            return self.confirmDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def addProduct(self, instance, *args):
        "close dialog box"
        try:
            self.confirmDialogBox.dismiss()
            try:
                productCode = str(self.codeText.text).strip()
                productName = (str(self.nameText.text).strip()).lower()
                productCprice = np.float64(
                    float(((self.cpriceText.text).strip()))
                ).round(decimals=2)
                productSprice = np.float64(
                    float(((self.spriceText.text).strip()))
                ).round(decimals=2)

                productQuantity = int((self.quantityText.text).strip())
            except Exception as e:
                self.productDataValidationPopUpBox()

                return
            else:
                self.model.addProductToDatabase(
                    productCode,
                    productName,
                    productCprice,
                    productSprice,
                    productQuantity,
                )
                # refresh the recycleview
                self.view.products_data.refresh_from_data()
                self.displayAllProducts()
                # clear the fields after adding the product
                self.codeText.text = ""
                self.nameText.text = ""
                self.cpriceText.text = ""
                self.spriceText.text = ""
                self.quantityText.text = ""
            self.productsOutOfStockInAdminPage()
            self.productsRuningOutOfStockInAdminPage()

        except Exception as e:
            Logs().logException(str(e))

    def productFieldsMustNotBeEmptyPopupBox(self):
        # buttons for the popup field
        try:
            self.okBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.notEmptyDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="All product fields must be filled.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.okBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.okBtn.bind(on_press=self.notEmptyDialogBox.dismiss)
            return self.notEmptyDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def productDataValidationPopUpBox(self):
        # buttons for the popup field
        try:
            self.validationOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.validateDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Product prices and Quantity fields takes only numbers",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.validationOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.validationOkBtn.bind(on_press=self.validateDialogBox.dismiss)
            return self.validateDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    # ============================ end of adding product to the database functionality===========================================

    # ====================editing the products in your database==================================

    def EditProductDialogPopUpBox(self):
        # buttons fof the popup field
        try:
            self.editCancelBtn = MDButton(
                MDButtonText(text="Cancel"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=(1, 0, 0, 1),
            )
            self.confirmEditBtn = MDButton(
                MDButtonText(text="Confirm"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("#735FF2"),
            )

            # input fields for the popup box
            # ---------top boxLayout that will contain the search boxt and the button------
            self.searchBoxlayout = MDBoxLayout(
                size_hint_y=None,
                height="40dp",
                spacing="5dp",
                padding=["0dp", "0dp", "50dp", "10dp"],
            )
            self.searchProductField = MDTextField(
                MDTextFieldHintText(
                    text="search product", text_color_normal="gray", height="40dp"
                ),
                text="",
            )
            self.searchBtnInEditDialogBox = MDButton(
                MDButtonIcon(icon="magnify"),
                style="filled",
                height="57dp",
                radius=["0dp", "10dp", "10dp", "0dp"],
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("32CD32"),
            )
            self.searchBoxlayout.add_widget(self.searchProductField)
            self.searchBoxlayout.add_widget(self.searchBtnInEditDialogBox)

            self.editProductCodeTextField = MDTextField(
                MDTextFieldHintText(text="product code", text_color_normal="gray"),
                text="",
            )
            self.editProductNameTextField = MDTextField(
                MDTextFieldHintText(text="product name", text_color_normal="gray"),
                text="",
            )
            self.editProductCpriceTextField = MDTextField(
                MDTextFieldHintText(
                    text="product cost price", text_color_normal="gray"
                ),
                text="",
            )
            self.editProductSpriceTextField = MDTextField(
                MDTextFieldHintText(
                    text="product selling price", text_color_normal="gray"
                ),
                text="",
            )
            self.editProductQuantityTextField = MDTextField(
                MDTextFieldHintText(text="product quantity", text_color_normal="gray"),
                text="",
            )

            self.editDialog = MDDialog(
                MDDialogHeadlineText(
                    text="EDIT PRODUCT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text fields for adding the products are kept
                MDDialogContentContainer(
                    self.searchBoxlayout,
                    self.editProductCodeTextField,
                    self.editProductNameTextField,
                    self.editProductCpriceTextField,
                    self.editProductSpriceTextField,
                    self.editProductQuantityTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.confirmEditBtn,
                    self.editCancelBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.productToSearchInEditPopUp = self.searchProductField
            self.editedCodeText = self.editProductCodeTextField
            self.editedNameText = self.editProductNameTextField
            self.editedCpriceText = self.editProductCpriceTextField
            self.editedSpriceText = self.editProductSpriceTextField
            self.editedQuantityText = self.editProductQuantityTextField

            # binding buttons to perform setting actions when pressed in the dialog box
            self.searchBtnInEditDialogBox.bind(on_press=self.searchProductToEdit)
            self.confirmEditBtn.bind(on_press=self.confirmToEditProductDialogPopUpBox)
            self.editCancelBtn.bind(on_press=self.editDialog.dismiss)
            return self.editDialog
        except Exception as e:
            Logs().logException(str(e))

    def openEditDialogPopUp(self):
        self.EditProductDialogPopUpBox().open()

    def searchProductToEdit(self, *args):
        try:
            productToSearch = (
                str(self.productToSearchInEditPopUp.text).strip()
            ).lower()
            _product = self.model.selectSearchedProductToEdit(productToSearch)
            # checking if the product to search does not exist
            if _product is None:
                self.searchProductNotFoundPopupBox()

            else:
                # product details
                try:
                    self._productId = str(_product[0])
                    _productCode = str(_product[1])
                    _productName = str(_product[2])
                    _productCprice = str(_product[3])
                    _productSprice = str(_product[4])
                    _productQuantity = str(_product[5])

                    # inserting the details to the popup dailogbox fields to be edited
                    self.editedCodeText.text = _productCode
                    self.editedNameText.text = _productName
                    self.editedCpriceText.text = _productCprice
                    self.editedSpriceText.text = _productSprice
                    self.editedQuantityText.text = _productQuantity
                except Exception as e:
                    Logs().logException(str(e))
                    pass
        except Exception as e:
            Logs().logException(str(e))

    def confirmToEditProductDialogPopUpBox(self, instance, *args):
        # checking to make sure all the fields are not empty
        try:
            if (
                str(self.editedCodeText.text)
                and str(self.editedNameText.text)
                and str(self.editedCpriceText.text)
                and str(self.editedSpriceText.text)
                and str(self.editedQuantityText.text)
            ) == "":
                self.productFieldsMustNotBeEmptyPopupBox()
                return

            # buttons for the popup field
            self.NoEditBtn = MDButton(
                MDButtonText(
                    text="No",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                    bold=True,
                ),
                style="text",
            )
            self.yesEditBtn = MDButton(
                MDButtonText(
                    text="yes",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )
            self.confirmEditDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="EDIT PRODUCT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Do you relly want to edit this product?.",
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.yesEditBtn,
                    self.NoEditBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.yesEditBtn.bind(on_press=self.confirmEdit)
            self.NoEditBtn.bind(on_press=self.confirmEditDialogBox.dismiss)
            return self.confirmEditDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def confirmEdit(self, *args):
        self.confirmEditDialogBox.dismiss()
        try:
            # taking the products details from the editing form
            pCode = str(self.editedCodeText.text).strip()
            pName = str(self.editedNameText.text).strip()
            pCprice = np.float64(float(str(self.editedCpriceText.text).strip())).round(
                decimals=2
            )
            pSprice = np.float64(float(str(self.editedSpriceText.text).strip())).round(
                decimals=2
            )
            pQuantity = int(str(self.editedQuantityText.text).strip())

            self.model.updateProduct(
                self._productId, pCode, pName, pCprice, pSprice, pQuantity
            )

            # refresh the recycleview
            self.view.products_data.refresh_from_data()
            self.displayAllProducts()
            # clear the fields after adding the product
            self.editedCodeText.text = ""
            self.editedNameText.text = ""
            self.editedCpriceText.text = ""
            self.editedSpriceText.text = ""
            self.editedQuantityText.text = ""
            self.productsOutOfStockInAdminPage()
            self.productsRuningOutOfStockInAdminPage()

        except Exception as e:
            self.productDataValidationPopUpBox()

    def searchProductNotFoundPopupBox(self):
        # buttons for the popup field
        try:
            self.notFoundOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.notFoundDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Product searched is not found.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.notFoundOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.notFoundOkBtn.bind(on_press=self.notFoundDialogBox.dismiss)
            return self.notFoundDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    # ====================end of editing the products in your database==================================

    # ================ deleating a product from the database=====================
    def deleteProductDialogBox(self):
        # buttons fof the popup field
        try:
            self.deleteProductNoBtn = MDButton(
                MDButtonText(
                    text="close",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )
            self.deleteProductBtn = MDButton(
                MDButtonText(
                    text="delete",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                    bold=True,
                ),
                style="text",
            )

            self.productToDeleteTextField = MDTextField(
                MDTextFieldHintText(
                    text="Enter product id or code", text_color_normal="gray"
                ),
                text="",
            )
            self.deleteDialog = MDDialog(
                MDDialogHeadlineText(
                    text="DELETE PRODUCT",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogContentContainer(
                    self.productToDeleteTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.deleteProductBtn,
                    self.deleteProductNoBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.productToDelete = self.productToDeleteTextField

            # binding buttons to perform setting actions when pressed in the dialog box
            self.deleteProductBtn.bind(
                on_press=self.confirmToDeleteProductDialogPopUpBox
            )
            self.deleteProductNoBtn.bind(on_press=self.deleteDialog.dismiss)
            return self.deleteDialog
        except Exception as e:
            Logs().logException(str(e))

    def openDeletePopuBox(self):
        self.deleteProductDialogBox().open()

    def deleteProductFromDatabase(self, *args):
        try:
            self.confirmDeleteDialogBox.dismiss()
            productToDelete_ = str(self.productToDelete.text).strip().lower()
            isDeleted = self.model.deleteProduct(productToDelete_)

            if isDeleted == "No":
                self.productNoDeletedPopUp()
                return
            self.productToDelete.text = ""
            # refresh the recycleview
            self.view.products_data.refresh_from_data()
            self.displayAllProducts()
            self.productsOutOfStockInAdminPage()
            self.productsRuningOutOfStockInAdminPage()
        except Exception as e:
            Logs().logException(str(e))

    def confirmToDeleteProductDialogPopUpBox(self, instance, *args):
        # checking to make sure the search fields not empty
        try:
            if str(self.productToDelete.text).strip() == "":
                self.productToDeleteFieldsMustNotBeEmptyPopupBox()
                return

            # buttons for the popup field
            self.NoDeleteBtn = MDButton(
                MDButtonText(
                    text="No",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                style="text",
            )
            self.yesDeleteBtn = MDButton(
                MDButtonText(
                    text="yes",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                ),
                style="text",
            )
            self.confirmDeleteDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="DELETE PRODUCT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Do you relly want to delete this product?.",
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.yesDeleteBtn,
                    self.NoDeleteBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.yesDeleteBtn.bind(on_press=self.deleteProductFromDatabase)
            self.NoDeleteBtn.bind(on_press=self.confirmDeleteDialogBox.dismiss)
            return self.confirmDeleteDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def productToDeleteFieldsMustNotBeEmptyPopupBox(self):
        # buttons for the popup field
        try:
            self.delOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.notEmptyProductDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Enter the product you want to delete.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.delOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.delOkBtn.bind(on_press=self.notEmptyProductDialogBox.dismiss)
            return self.notEmptyProductDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def productNoDeletedPopUp(self):
        # buttons for the popup field
        try:
            self.notDelededOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.notDelededDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_bg_color="Custom",
                    md_bg_color=(1, 0, 0, 1),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Product not found.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.notDelededOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.notDelededOkBtn.bind(on_press=self.notDelededDialogBox.dismiss)
            return self.notDelededDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    # ----------------------------------user window section================
    def AddUserDialogPopUpBox(self):
        """This is a popup dialog page that pops up when you click on the
        add button in the user page for you to add the user you want to
        to the database
        """
        try:
            # buttons of the popup field
            self.userCancelBtn = MDButton(
                MDButtonText(text="Cancel"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=(1, 0, 0, 1),
            )
            self.userAddBtn = MDButton(
                MDButtonText(text="Add"),
                MDButtonIcon(
                    icon="plus", theme_icon_color="Custom", icon_color="white"
                ),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("#735FF2"),
            )

            # input fields for the popup box
            self.userFirstNameTextField = MDTextField(
                MDTextFieldHintText(text="user first name", text_color_normal="gray"),
                text="",
                multiline=False,
            )
            self.userLastNameTextField = MDTextField(
                MDTextFieldHintText(text="user last name", text_color_normal="gray"),
                text="",
                multiline=False,
            )
            self.userPasswordTextField = MDTextField(
                MDTextFieldHintText(text="password", text_color_normal="gray"),
                text="",
                multiline=False,
            )
            self.userDesignationTextField = MDTextField(
                MDTextFieldHintText(
                    text="designation (admin or operator)", text_color_normal="gray"
                ),
                text="",
                multiline=False,
            )

            self.userContactTextField = MDTextField(
                MDTextFieldHintText(text="contact", text_color_normal="gray"),
                MDTextFieldMaxLengthText(max_text_length=10),
                text="",
                multiline=False,
            )

            self.addUserDialogPopUp = MDDialog(
                MDDialogHeadlineText(
                    text="ADD USER",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text fields for adding the products are kept
                MDDialogContentContainer(
                    self.userFirstNameTextField,
                    self.userLastNameTextField,
                    self.userPasswordTextField,
                    self.userDesignationTextField,
                    self.userContactTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.userAddBtn,
                    self.userCancelBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.userFirstNameText = self.userFirstNameTextField
            self.userLastNameText = self.userLastNameTextField
            self.userPasswordText = self.userPasswordTextField
            self.userDesignationText = self.userDesignationTextField
            self.userContactText = self.userContactTextField

            self.userAddBtn.bind(on_press=self.confirmToAddUserDialogPopUpBox)
            self.userCancelBtn.bind(on_press=self.addUserDialogPopUp.dismiss)
            return self.addUserDialogPopUp
        except Exception as e:
            Logs().logException(str(e))

    def openAddUserDialogPopUpBox(self):
        self.AddUserDialogPopUpBox().open()

    def confirmToAddUserDialogPopUpBox(self, instance, *args):
        # checking to make sure all the fields are not empty
        try:
            if (
                str(self.userFirstNameText.text)
                and str(self.userLastNameText.text)
                and str(self.userPasswordText.text)
                and str(self.userDesignationText.text)
                and str(self.userContactText.text)
            ) == "":
                self.userFieldsMustNotBeEmptyPopupBox()
                return

            # buttons for the popup field
            self.userNoBtn = MDButton(
                MDButtonText(
                    text="No",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                style="text",
            )
            self.userYesBtn = MDButton(
                MDButtonText(
                    text="yes",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                ),
                style="text",
            )
            self.confirmAddDialogBox = MDDialog(
                MDDialogHeadlineText(text="ADD USER"),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Do you relly want to add this user?.",
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.userYesBtn,
                    self.userNoBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.userYesBtn.bind(on_press=self.addUser)
            self.userNoBtn.bind(on_press=self.confirmAddDialogBox.dismiss)
            return self.confirmAddDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def userFieldsMustNotBeEmptyPopupBox(self):
        # buttons for the popup field
        try:
            self.okBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.notEmptyDialogBox = MDDialog(
                MDDialogHeadlineText(text="ERROR"),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="All user fields must be filled.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.okBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.okBtn.bind(on_press=self.notEmptyDialogBox.dismiss)
            return self.notEmptyDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def addUser(self, instance, *args):
        "close dialog box"
        self.confirmAddDialogBox.dismiss()
        try:
            userFName = (str(self.userFirstNameText.text).strip()).lower()
            userLName = (str(self.userLastNameText.text).strip()).lower()
            userPassword = str(self.userPasswordText.text).strip()
            userDesignation = (str(self.userDesignationText.text).strip()).lower()
            userContact = str(self.userContactText.text).strip()

            if userFName == "":
                self.userDataValidationPopUpBox()
            if userLName == "":
                self.userDataValidationPopUpBox()

            elif userPassword == "":
                self.userDataValidationPopUpBox()

            elif userContact == "":
                self.userDataValidationPopUpBox()

            elif (str(userDesignation.lower()) != "admin") and (
                str(userDesignation.lower()) != "operator"
            ):
                self.designationErrorPopuBox()
            else:
                self.model.addUserToDatabase(
                    userFName, userLName, userPassword, userDesignation, userContact
                )
                # refresh the recycleview
                self.view.ids["user_table"].refresh_from_data()
                self.displayAllUsers()
                # clear the fields after adding the product
                self.userFirstNameText.text = ""
                self.userLastNameText.text = ""
                self.userPasswordText.text = ""
                self.userDesignationText.text = ""
                self.userContactText.text = ""
        except Exception as e:
            self.userDataValidationPopUpBox()

            return

    def userDataValidationPopUpBox(self):
        # buttons for the popup field
        try:
            self.validationOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.validateDialogBox = MDDialog(
                MDDialogHeadlineText(text="ERROR"),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="user name and password fields must not be empty",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.validationOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.validationOkBtn.bind(on_press=self.validateDialogBox.dismiss)
            return self.validateDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def designationErrorPopuBox(self):
        # buttons for the popup field
        try:
            self.designationOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.designationDialogBox = MDDialog(
                MDDialogHeadlineText(text="ERROR"),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="designation must be 'admin' or 'operator'",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.designationOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.designationOkBtn.bind(on_press=self.designationDialogBox.dismiss)
            return self.designationDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def displayAllUsers(self):
        try:
            allAvailableUsers = self.model.selectAllUsers()
            # refrencing the recycle view where all the data will be displayed
            recycleviewToDisplayData = self.view.ids["user_table"]

            dataToDisplay = []
            # display information on the recycle view(tabel containing the list of users) if there are no users in the system
            if allAvailableUsers[0] == "None":
                recycleviewToDisplayData.data = [
                    {"text": "There are no users curently in the system"}
                ]
            else:
                """ displaying all the available users in the database"""
                for user in allAvailableUsers:
                    try:
                        userId = {"text": str(user[0])}
                        userFName = {"text": str(user[1])}
                        userLName = {"text": str(user[2])}
                        userPassword = {"text": str(user[3])}
                        userDesignation = {"text": str(user[4])}
                        userContact = {"text": str(user[5])}

                        dataToDisplay.append(userId)
                        dataToDisplay.append(userFName)
                        dataToDisplay.append(userLName)
                        dataToDisplay.append(userPassword)
                        dataToDisplay.append(userDesignation)
                        dataToDisplay.append(userContact)
                    except Exception as e:
                        pass
                # populating the table with the selected data
                recycleviewToDisplayData.refresh_from_data()
                recycleviewToDisplayData.data = dataToDisplay
        except Exception as e:
            Logs().logException(str(e))

    def searchUserByIdOrName(self, userIdOrName, userRecycleBox):
        """This function is called by the search button in the user window
        to display
        1. all the user if the search box is empty or 'all'
        2. display a particular user given its id,name or product bar code
        """
        try:
            selectedUsers = self.model.selectSearchedUser(
                (str(userIdOrName).lower()).strip()
            )

            # creating an object of the recycle box where all the users data will be displayed
            refrencedRecycleview = userRecycleBox

            # giving a message to tell the user that the product that he or she is trying to search those not exist
            if len(selectedUsers) == 0:
                refrencedRecycleview.refresh_from_data()
                refrencedRecycleview.data = [
                    {
                        "text": f"There is no user in the system with name or id '{userIdOrName}'"
                    }
                ]

            else:
                """populating the recycle view with the data of
                the searched user"""

                listOfsearchedUsers = []
                for user in selectedUsers:
                    try:
                        userId = {"text": str(user[0])}
                        userFName = {"text": str(user[1])}
                        userLName = {"text": str(user[2])}
                        userPassword = {"text": str(user[3])}
                        userDesignation = {"text": str(user[4])}
                        userContact = {"text": str(user[5])}

                        listOfsearchedUsers.append(userId)
                        listOfsearchedUsers.append(userFName)
                        listOfsearchedUsers.append(userLName)
                        listOfsearchedUsers.append(userPassword)
                        listOfsearchedUsers.append(userDesignation)
                        listOfsearchedUsers.append(userContact)
                    except Exception as e:
                        pass

                # refreshing the recycleview and populating it with data searched
                refrencedRecycleview.refresh_from_data()
                refrencedRecycleview.data = listOfsearchedUsers
        except Exception as e:
            Logs().logException(str(e))

    # ====================editing the user in your database==================================

    def EditUserDialogPopUpBox(self):
        # buttons fof the popup field
        try:
            self.editUserCancelBtn = MDButton(
                MDButtonText(text="Cancel"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=(1, 0, 0, 1),
            )
            self.confirmUserEditBtn = MDButton(
                MDButtonText(text="Confirm"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("#735FF2"),
            )

            # input fields for the popup box
            # ---------top boxLayout that will contain the search boxt and the button------
            self.searchUserBoxlayout = MDBoxLayout(
                size_hint_y=None,
                height="40dp",
                spacing="5dp",
                padding=["0dp", "0dp", "50dp", "10dp"],
            )
            self.searchUserField = MDTextField(
                MDTextFieldHintText(
                    text="search user", text_color_normal="gray", height="40dp"
                ),
                text="",
            )
            self.searchBtnInUserEditDialogBox = MDButton(
                MDButtonIcon(icon="magnify"),
                style="filled",
                height="57dp",
                radius=["0dp", "10dp", "10dp", "0dp"],
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("32CD32"),
            )
            self.searchUserBoxlayout.add_widget(self.searchUserField)
            self.searchUserBoxlayout.add_widget(self.searchBtnInUserEditDialogBox)

            self.editUserFirstNameTextField = MDTextField(
                MDTextFieldHintText(text="user first name", text_color_normal="gray"),
                text="",
            )
            self.editUserLastNameTextField = MDTextField(
                MDTextFieldHintText(text="user last name", text_color_normal="gray"),
                text="",
            )
            self.editUserPasswordTextField = MDTextField(
                MDTextFieldHintText(text="password", text_color_normal="gray"),
                text="",
            )
            self.editUserDesignationTextField = MDTextField(
                MDTextFieldHintText(text="designation", text_color_normal="gray"),
                text="",
            )
            self.editUserContactTextField = MDTextField(
                MDTextFieldHintText(text="contact", text_color_normal="gray"),
                text="",
            )

            self.editUserDialog = MDDialog(
                MDDialogHeadlineText(
                    text="EDIT USER",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text fields for editing the user are kept
                MDDialogContentContainer(
                    self.searchUserBoxlayout,
                    self.editUserFirstNameTextField,
                    self.editUserLastNameTextField,
                    self.editUserPasswordTextField,
                    self.editUserDesignationTextField,
                    self.editUserContactTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.confirmUserEditBtn,
                    self.editUserCancelBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.userToSearchInEditPopUp = self.searchUserField
            self.editedFNameText = self.editUserFirstNameTextField
            self.editedLNameText = self.editUserLastNameTextField
            self.editedPasswordText = self.editUserPasswordTextField
            self.editedDesignationText = self.editUserDesignationTextField
            self.editedContactText = self.editUserContactTextField

            # binding buttons to perform setting actions when pressed in the dialog box
            self.searchBtnInUserEditDialogBox.bind(on_press=self.searchUserToEdit)
            self.confirmUserEditBtn.bind(on_press=self.confirmToEditUserDialogPopUpBox)
            self.editUserCancelBtn.bind(on_press=self.editUserDialog.dismiss)
            return self.editUserDialog
        except Exception as e:
            Logs().logException(str(e))

    def openEditUserDialogPopUp(self):
        self.EditUserDialogPopUpBox().open()

    def searchUserToEdit(self, *args):
        try:
            userToSearch = (str(self.userToSearchInEditPopUp.text).strip()).lower()
            _user = self.model.selectSearchedUserToEdit(userToSearch)
            # checking if the product to search does not exist
            if _user is None:
                self.searchUserNotFoundPopupBox()

            else:
                # USER details
                try:
                    self._userId = str(_user[0])
                    _userfName = str(_user[1])
                    _userlName = str(_user[2])
                    _userPassword = str(_user[3])
                    _userDesignation = str(_user[4])
                    _userContact = str(_user[5])

                    # inserting the details to the popup dailogbox fields to be edited
                    self.editedFNameText.text = _userfName
                    self.editedLNameText.text = _userlName
                    self.editedPasswordText.text = _userPassword
                    self.editedDesignationText.text = _userDesignation
                    self.editedContactText.text = _userContact
                except Exception as e:
                    Logs().logException(str(e))
        except Exception as e:
            Logs().logException(str(e))

    def confirmToEditUserDialogPopUpBox(self, instance, *args):
        # checking to make sure all the fields are not empty
        try:
            if (
                str(self.editedFNameText.text)
                and str(self.editedLNameText.text)
                and str(self.editedPasswordText.text)
                and str(self.editedDesignationText.text)
                and str(self.editedContactText.text)
            ) == "":
                self.userFieldsMustNotBeEmptyPopupBox()
                return

            # buttons for the popup field
            self.EditNoUserBtn = MDButton(
                MDButtonText(
                    text="No",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                    bold=True,
                ),
                style="text",
            )
            self.EditYesUserBtn = MDButton(
                MDButtonText(
                    text="yes",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )
            self.confirmEditUserDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="EDIT PRODUCT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Do you relly want to edit this product?.",
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.EditYesUserBtn,
                    self.EditNoUserBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.EditYesUserBtn.bind(on_press=self.confirmEditUser)
            self.EditNoUserBtn.bind(on_press=self.confirmEditUserDialogBox.dismiss)
            return self.confirmEditUserDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def confirmEditUser(self, *args):
        self.confirmEditUserDialogBox.dismiss()
        try:
            # taking the user details from the editing form
            userfName = str(self.editedFNameText.text).strip()
            userlName = str(self.editedLNameText.text).strip()
            userPassword = str(self.editedPasswordText.text).strip()
            userDesignation = str(self.editedDesignationText.text).strip()
            userContact = str(self.editedContactText.text).strip()

            if (str(userDesignation.lower()) != "admin") and (
                str(userDesignation.lower()) != "operator"
            ):
                self.designationErrorPopuBox()
            else:
                self.model.updateUser(
                    self._userId,
                    userfName,
                    userlName,
                    userPassword,
                    userDesignation,
                    userContact,
                )

                # refresh the recycleview
                self.view.ids["user_table"].refresh_from_data()
                self.displayAllUsers()
                # clear the fields after adding the product
                self.editedFNameText.text = ""
                self.editedLNameText.text = ""
                self.editedPasswordText.text = ""
                self.editedDesignationText.text = ""
                self.editedContactText.text = ""
        except Exception as e:
            self.userDataValidationPopUpBox()

    def searchUserNotFoundPopupBox(self):
        # buttons for the popup field
        try:
            self.userNotFoundOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.userNotFoundDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="user searched is not found.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.userNotFoundOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.userNotFoundOkBtn.bind(on_press=self.userNotFoundDialogBox.dismiss)
            return self.userNotFoundDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    # ====================end of editing the user in your database==================================

    # ================ deleating a user from the database=====================
    def deleteUserDialogBox(self):
        # buttons fof the popup field
        try:
            self.deleteUserNoBtn = MDButton(
                MDButtonText(
                    text="close",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )
            self.deleteUserBtn = MDButton(
                MDButtonText(
                    text="delete",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                    bold=True,
                ),
                style="text",
            )

            self.userToDeleteTextField = MDTextField(
                MDTextFieldHintText(text="Enter user id", text_color_normal="gray"),
                text="",
            )
            self.deleteUserDialog = MDDialog(
                MDDialogHeadlineText(
                    text="DELETE USER",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogContentContainer(
                    self.userToDeleteTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.deleteUserBtn,
                    self.deleteUserNoBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.userToDelete = self.userToDeleteTextField

            # binding buttons to perform setting actions when pressed in the dialog box
            self.deleteUserBtn.bind(on_press=self.confirmToDeleteUserDialogPopUpBox)
            self.deleteUserNoBtn.bind(on_press=self.deleteUserDialog.dismiss)
            return self.deleteUserDialog
        except Exception as e:
            Logs().logException(str(e))

    def openDeleteUserPopuBox(self):
        self.deleteUserDialogBox().open()

    def deleteUserFromDatabase(self, *args):
        try:
            self.userConfirmDeleteDialogBox.dismiss()
            userToDelete_ = str(self.userToDelete.text).strip().lower()
            isDeleted = self.model.deleteUser(userToDelete_)

            if isDeleted == "No":
                self.userNotDeletedPopUp()
                return
            self.userToDelete.text = ""
            # refresh the recycleview
            self.view.ids["user_table"].refresh_from_data()
            self.displayAllUsers()
        except Exception as e:
            Logs().logException(str(e))

    def confirmToDeleteUserDialogPopUpBox(self, instance, *args):
        # checking to make sure the search fields not empty
        try:
            if str(self.userToDelete.text).strip() == "":
                self.userToDeleteFieldsMustNotBeEmptyPopupBox()
                return

            # buttons for the popup field
            self.userNoDeleteBtn = MDButton(
                MDButtonText(
                    text="No",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                style="text",
            )
            self.userYesDeleteBtn = MDButton(
                MDButtonText(
                    text="yes",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                ),
                style="text",
            )
            self.userConfirmDeleteDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="DELETE PRODUCT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Do you relly want to delete this product?.",
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.userYesDeleteBtn,
                    self.userNoDeleteBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.userYesDeleteBtn.bind(on_press=self.deleteUserFromDatabase)
            self.userNoDeleteBtn.bind(on_press=self.userConfirmDeleteDialogBox.dismiss)
            return self.userConfirmDeleteDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def userToDeleteFieldsMustNotBeEmptyPopupBox(self):
        # buttons for the popup field
        try:
            self.userdelOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.usernotEmptyProductDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="Enter the id of the user you want to delete.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.userdelOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.userdelOkBtn.bind(on_press=self.usernotEmptyProductDialogBox.dismiss)
            return self.usernotEmptyProductDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    def userNotDeletedPopUp(self):
        # buttons for the popup field
        try:
            self.userNotDelededOkBtn = MDButton(
                MDButtonText(
                    text="Ok",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#735FF2"),
                    bold=True,
                ),
                style="text",
            )

            self.userNotDelededDialogBox = MDDialog(
                MDDialogHeadlineText(
                    text="ERROR",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                ),
                # this is where the text field for deleting the products is kept
                MDDialogSupportingText(
                    text="User not found.",
                    halign="left",
                    theme_text_color="Custom",
                    text_color="red",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.userNotDelededOkBtn,
                    spacing="8dp",
                ),
                size_hint=(0.1, 0.4),
                auto_dismiss=False,
            )
            # binding buttons to perform setting actions when pressed in the dialog box
            self.userNotDelededOkBtn.bind(on_press=self.userNotDelededDialogBox.dismiss)
            return self.userNotDelededDialogBox.open()
        except Exception as e:
            Logs().logException(str(e))

    # ========================sales section=======================
    def displayAllSales(self):
        try:
            allAvailableSales = self.model.selectAllSales()
            # sorting all the sale product base on their code and displaying the sum all the details
            sumOfSales = dict()
            # get unigue codes of the sales made
            for sale in allAvailableSales:
                if sale[1] in sumOfSales.keys():  # the product code
                    # updating it quantity and profit
                    priviewsQt = sumOfSales[f"{sale[1]}"][3]
                    priviewsProfit = sumOfSales[f"{sale[1]}"][5]
                    qtToAdd = sale[3]
                    profitToAdd = sale[5]
                    # updated
                    sumOfSales[f"{sale[1]}"][3] = int(priviewsQt) + int(qtToAdd)
                    sumOfSales[f"{sale[1]}"][5] = decimal.Decimal(
                        str(float(priviewsProfit) + float(profitToAdd))
                    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                else:
                    # creating a sale with it code as the key
                    sumOfSales[f"{sale[1]}"] = list(sale)
            # refrencing the recycle view where all the data will be displayed
            recycleviewToDisplaySalesData = self.view.ids["sales_products_table"]

            salesDataToDisplay = []

            # display information on the recycle view(tabel containing the list of users) if there are no users in the system
            if allAvailableSales[0] == "None":
                recycleviewToDisplaySalesData.data = [
                    {"text": "There are no sales curently in the system"}
                ]
            else:
                """ displaying all the available sales in the database"""
                for key in sumOfSales.keys():
                    try:
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][1])}
                        )  # ===>Sale code
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][2])}
                        )  # ===>product name
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][3])}
                        )  # ===>Sale qt
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][5])}
                        )  # ===>profit made

                    except Exception as e:
                        print(e)
                        pass
                # populating the table with the selected data
                recycleviewToDisplaySalesData.refresh_from_data()
                recycleviewToDisplaySalesData.data = salesDataToDisplay
        except Exception as e:
            Logs().logException(str(e))

    def showAllSales(self, selectItemObject):
        selectItemObject.values = ["All sales"]

    def filterByYear(self, selectItemObject):
        try:
            years = self.model.selectSalesByYear()
            selectItemObject.values = sorted(
                [str(yea[0]) for yea in years], reverse=True
            )
        except Exception as e:
            Logs().logException(str(e))

    def filterByMonth(self, selectItemObject):
        try:
            months = self.model.selectSalesByMonth()
            # sorting the months
            monthsDictionary = dict()
            for mon in months:
                # spliting the month into its name and yeat
                splitMonth = str(mon[0]).strip().split(" ")
                monthName = splitMonth[0]
                year = splitMonth[-1]

                if str(monthName) == "Jan":
                    key = int(f"{year}{1}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Feb":
                    key = int(f"{year}{2}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Mar":
                    key = int(f"{year}{3}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Apr":
                    key = int(f"{year}{4}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "May":
                    key = int(f"{year}{5}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Jun":
                    key = int(f"{year}{6}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Jul":
                    key = int(f"{year}{7}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Aug":
                    key = int(f"{year}{8}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Sep":
                    key = int(f"{year}{9}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Oct":
                    key = int(f"{year}{10}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Nov":
                    key = int(f"{year}{11}")
                    monthsDictionary[f"{key}"] = str(mon[0])
                elif str(monthName) == "Dec":
                    key = int(f"{year}{12}")
                    monthsDictionary[f"{key}"] = str(mon[0])

            sortedMothsKeys = [sorted((monthsDictionary.keys()), reverse=True)]
            sortedMonths = []
            for k in sortedMothsKeys[0]:
                sortedMonths.append(str(monthsDictionary[f"{k}"]))

            selectItemObject.values = sortedMonths
        except Exception as e:
            Logs().logException(str(e))

    def filterByDay(self, selectItemObject):
        try:
            days = self.model.selectSalesByDay()

            # sorting the days
            daysDictionary = dict()
            for day in days:
                # spliting the days into its day, moth,and year
                splitDay = str(day[0]).strip().split(" ")
                dayNumber = splitDay[0]
                monthName = splitDay[1]
                year = splitDay[-1]
                # assigning a number to each day
                if str(monthName) == "Jan":
                    key = int(f"{year}{1}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Feb":
                    key = int(f"{year}{2}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Mar":
                    key = int(f"{year}{3}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Apr":
                    key = int(f"{year}{4}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "May":
                    key = int(f"{year}{5}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Jun":
                    key = int(f"{year}{6}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Jul":
                    key = int(f"{year}{7}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Aug":
                    key = int(f"{year}{8}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Sep":
                    key = int(f"{year}{9}{day}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Oct":
                    key = int(f"{year}{10}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Nov":
                    key = int(f"{year}{11}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])
                elif str(monthName) == "Dec":
                    key = int(f"{year}{12}{dayNumber}")
                    daysDictionary[f"{key}"] = str(day[0])

            sortedDaysKeys = [sorted((daysDictionary.keys()), reverse=True)]
            sortedDays = []
            for k in sortedDaysKeys[0]:
                sortedDays.append(str(daysDictionary[f"{k}"]))

            selectItemObject.values = sortedDays
        except Exception as e:
            Logs().logException(str(e))

    def searchSalesByYearMonthDay(self, text):
        try:
            AvailableSales = self.model.selectSales(text)
            # sorting all the sale product base on their code and displaying the sum all the details
            sumOfSales = dict()
            # get unigue codes of the sales made
            for sale in AvailableSales:
                if sale[1] in sumOfSales.keys():  # the product code
                    # updating it quantity and profit
                    priviewsQt = sumOfSales[f"{sale[1]}"][3]
                    priviewsProfit = sumOfSales[f"{sale[1]}"][5]
                    qtToAdd = sale[3]
                    profitToAdd = sale[5]
                    # updated
                    sumOfSales[f"{sale[1]}"][3] = int(priviewsQt) + int(qtToAdd)
                    sumOfSales[f"{sale[1]}"][5] = decimal.Decimal(
                        str(float(priviewsProfit) + float(profitToAdd))
                    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                else:
                    # creating a sale with it code as the key
                    sumOfSales[f"{sale[1]}"] = list(sale)
            # refrencing the recycle view where all the data will be displayed
            recycleviewToDisplaySalesData = self.view.ids["sales_products_table"]

            salesDataToDisplay = []

            # display information on the recycle view(tabel containing the list of users) if there are no users in the system
            if AvailableSales[0] == "None":
                recycleviewToDisplaySalesData.data = [
                    {"text": f"There are no sales curently in the system with {text}"}
                ]
            else:
                """ displaying all the available sales in the database"""
                for key in sumOfSales.keys():
                    try:
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][1])}
                        )  # ===>Sale code
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][2])}
                        )  # ===>product name
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][3])}
                        )  # ===>Sale qt
                        salesDataToDisplay.append(
                            {"text": str(sumOfSales[key][5])}
                        )  # ===>profit made

                    except Exception as e:
                        return
                # populating the table with the selected data
                recycleviewToDisplaySalesData.refresh_from_data()
                recycleviewToDisplaySalesData.data = salesDataToDisplay
        except Exception as e:
            Logs().logException(str(e))

    def searchSalesProduct(self, selectItemObject):
        try:
            text = str(selectItemObject.text).strip()
            if text == "All sales":
                self.displayAllSales()
            # search by year month or day
            else:
                self.searchSalesByYearMonthDay(text)
        except Exception as e:
            Logs().logException(str(e))

    # ========================end of sales section=======================

    # =========================company details===========================
    def EditCompanyNameDialogPopUpBox(self):
        # buttons fof the popup field
        try:
            self.editCnameCancelBtn = MDButton(
                MDButtonText(text="Cancel"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=(1, 0, 0, 1),
            )
            self.confirmNameEditBtn = MDButton(
                MDButtonText(text="Confirm"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("#735FF2"),
            )

            # input fields for the popup box

            self.newNameTextField = MDTextField(
                MDTextFieldHintText(text="Enter new name", text_color_normal="gray"),
                text="",
            )

            self.editcNameDialog = MDDialog(
                MDDialogHeadlineText(
                    text="EDIT COMPANY NAME",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text fields for editing the user are kept
                MDDialogContentContainer(
                    self.newNameTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.confirmNameEditBtn,
                    self.editCnameCancelBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.newName = self.newNameTextField

            # binding buttons to perform setting actions when pressed in the dialog box
            self.confirmNameEditBtn.bind(on_press=self.editCompanyName)
            self.editCnameCancelBtn.bind(on_press=self.editcNameDialog.dismiss)
            return self.editcNameDialog.open()
        except Exception as e:
            Logs().logException(str(e))

    def editCompanyName(self, *args):
        try:
            newName = str(self.newName.text).strip()
            if newName == "":
                pass
            else:
                # update the name in the db
                self.model.updateCompanyName(newName)
                self.labelCompanyDetails()
                self.editcNameDialog.dismiss()
        except Exception as e:
            Logs().logException(str(e))

    def EditCompanyLocationDialogPopUpBox(self):
        # buttons fof the popup field
        try:
            self.editClocationCancelBtn = MDButton(
                MDButtonText(text="Cancel"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=(1, 0, 0, 1),
            )
            self.confirmCLocationEditBtn = MDButton(
                MDButtonText(text="Confirm"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("#735FF2"),
            )

            # input fields for the popup box

            self.newLocationTextField = MDTextField(
                MDTextFieldHintText(
                    text="Enter new location", text_color_normal="gray"
                ),
                text="",
            )

            self.editCLocationDialog = MDDialog(
                MDDialogHeadlineText(
                    text="EDIT COMPANY LOCATION",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text fields for editing the user are kept
                MDDialogContentContainer(
                    self.newLocationTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.confirmCLocationEditBtn,
                    self.editClocationCancelBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.newLocation = self.newLocationTextField

            # binding buttons to perform setting actions when pressed in the dialog box
            self.confirmCLocationEditBtn.bind(on_press=self.editCompanyLocation)
            self.editClocationCancelBtn.bind(on_press=self.editCLocationDialog.dismiss)
            return self.editCLocationDialog.open()
        except Exception as e:
            Logs().logException(str(e))

    def editCompanyLocation(self, *args):
        try:
            newLocat = str(self.newLocation.text).strip()
            if newLocat == "":
                pass
            else:
                # update the name in the db
                self.model.updateCompanyLocation(newLocat)
                self.labelCompanyDetails()
                self.editCLocationDialog.dismiss()
        except Exception as e:
            Logs().logException(str(e))

    def EditCompanyContactDialogPopUpBox(self):
        # buttons fof the popup field
        try:
            self.editCContactCancelBtn = MDButton(
                MDButtonText(text="Cancel"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=(1, 0, 0, 1),
            )
            self.confirmCContactEditBtn = MDButton(
                MDButtonText(text="Confirm"),
                style="filled",
                theme_bg_color="Custom",
                md_bg_color=get_color_from_hex("#735FF2"),
            )

            # input fields for the popup box

            self.newContactTextField = MDTextField(
                MDTextFieldHintText(text="Enter new contact", text_color_normal="gray"),
                text="",
            )

            self.editCContactDialog = MDDialog(
                MDDialogHeadlineText(
                    text="EDIT COMPANY CONTACT",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("32CD32"),
                ),
                # this is where the text fields for editing the user are kept
                MDDialogContentContainer(
                    self.newContactTextField,
                    orientation="vertical",
                    spacing="8dp",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    self.confirmCContactEditBtn,
                    self.editCContactCancelBtn,
                    spacing="8dp",
                ),
                size_hint=(0.3, 0.5),
                auto_dismiss=False,
            )
            self.newContact = self.newContactTextField

            # binding buttons to perform setting actions when pressed in the dialog box
            self.confirmCContactEditBtn.bind(on_press=self.editCompanyContact)
            self.editCContactCancelBtn.bind(on_press=self.editCContactDialog.dismiss)
            return self.editCContactDialog.open()
        except Exception as e:
            Logs().logException(str(e))

    def editCompanyContact(self, *args):
        try:
            newCont = str(self.newContact.text).strip()
            if newCont == "":
                pass
            else:
                # update the name in the db
                self.model.updateCompanyContact(newCont)
                self.labelCompanyDetails()
                self.editCContactDialog.dismiss()
        except Exception as e:
            Logs().logException(str(e))

    def labelCompanyDetails(self):
        # this fetches the company data and lable them on the store details page
        try:
            details = self.model.returningCompanyDetails()
            self.view.ids.companyName.text = str(details[0][1])
            self.view.ids.companyLocation.text = str(details[0][2])
            self.view.ids.companyContact.text = str(details[0][3])
        except Exception as e:
            Logs().logException(str(e))

    def productsOutOfStockInAdminPage(self):
        out = self.model.selectAllOutOfStockProducts()
        namesOfProducts = []
        if len(out) == 0:
            namesOfProducts.append({"text": "No product is out of stock"})
        else:
            for prod in out:
                try:
                    namesOfProducts.append({"text": str(prod[2])})
                except Exception as e:
                    Logs().logException(str(e))

        self.view.ids.adminStockOutData.data = namesOfProducts

    def productsRuningOutOfStockInAdminPage(self):
        out = self.model.selectAllRuningOutOfStockProducts()
        namesOfProducts = []
        if len(out) == 0:
            namesOfProducts.append({"text": "No product is out of stock"})
        else:
            for prod in out:
                if int(prod[-1]) == 0:
                    pass
                else:
                    try:
                        namesOfProducts.append({"text": str(prod[2])})
                    except Exception as e:
                        Logs().logException(str(e))

        self.view.ids.adminStockRuningOutData.data = namesOfProducts
