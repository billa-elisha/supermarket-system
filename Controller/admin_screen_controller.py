from kivy.uix.gridlayout import product
from kivy.properties import ObjectProperty
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
import numpy as np
import decimal as decimal


class AdminScreenController:
    def __init__(self, model):
        self.model = model
        self.view = View.AdminScreen.admin_screen.AdminScreenView(
            controller=self, model=self.model
        )
        self.displayAllProducts()

    def get_view(self):
        return self.view

    def get_parent(self, nav_screen_manager, button):
        button_name = button.text
        if button_name == "Products":
            nav_screen_manager.current = "products screen"
            return
        if button_name == "Sales":
            nav_screen_manager.current = "sales screen"
            return
        if button_name == "Analysis":
            nav_screen_manager.current = "analysis screen"
            return
        if button_name == "Users":
            nav_screen_manager.current = "users screen"
            return

        # print(v.text)
        # iii.current = "products screen"

    def searchProductByIdOrName(self, productIdOrName):
        """This function is called by the search button in the products window
        to display
        1. all the product if the search box is empty or 'all'
        2. display a particular product given its id,name or product bar code
        """
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
                    pass

            # refreshing the recycleview and populating it with data searched
            refrencedRecycleview.refresh_from_data()
            refrencedRecycleview.data = listOfsearchedProducts

    def displayAllProducts(self):
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
                    pass
            # populating the table with the selected data
            recycleviewToDisplayData.refresh_from_data()
            recycleviewToDisplayData.data = dataToDisplay

    # ============================adding product to the database===========================================

    def AddProductDialogPopUpBox(self):
        """This is a popup dialog page that pops up when you click on the
        add button in the products page for you to add the product you want to
        to the database
        """
        # buttons of the popup field
        self.cancelBtn = MDButton(
            MDButtonText(text="Cancel"),
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(1, 0, 0, 1),
        )
        self.addBtn = MDButton(
            MDButtonText(text="Add"),
            MDButtonIcon(icon="plus", theme_icon_color="Custom", icon_color="white"),
            style="filled",
            theme_bg_color="Custom",
            md_bg_color=(0, 0, 1, 1),
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
            MDTextFieldHintText(text="product cost price", text_color_normal="gray"),
            text="",
            multiline=False,
        )
        self.productSpriceTextField = MDTextField(
            MDTextFieldHintText(text="product selling price", text_color_normal="gray"),
            text="",
            multiline=False,
        )
        self.productQuantityTextField = MDTextField(
            MDTextFieldHintText(text="product quantity", text_color_normal="gray"),
            text="",
            multiline=False,
        )

        self.addDialogPopUp = MDDialog(
            MDDialogHeadlineText(text="ADD PRODUCT"),
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

    def openAddProductDialogPopUpBox(self):
        self.AddProductDialogPopUpBox().open()

    def confirmToAddProductDialogPopUpBox(self, instance, *args):
        # checking to make sure all the fields are not empty

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
                text_color=(0, 0, 1, 1),
            ),
            style="text",
        )
        self.confirmDialogBox = MDDialog(
            MDDialogHeadlineText(text="ADD PRODUCT"),
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

    def addProduct(self, instance, *args):
        "close dialog box"
        self.confirmDialogBox.dismiss()
        try:
            productCode = str(self.codeText.text).strip()
            productName = str(self.nameText.text).strip()
            productCprice = np.float64(float(((self.cpriceText.text).strip()))).round(
                decimals=2
            )
            productSprice = np.float64(float(((self.spriceText.text).strip()))).round(
                decimals=2
            )

            productQuantity = int((self.quantityText.text).strip())
        except Exception as e:
            self.productDataValidationPopUpBox()
            print(e)

            return
        else:
            self.model.addProductToDatabase(
                productCode, productName, productCprice, productSprice, productQuantity
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

    def productFieldsMustNotBeEmptyPopupBox(self):
        # buttons for the popup field
        self.okBtn = MDButton(
            MDButtonText(
                text="Ok",
                theme_text_color="Custom",
                text_color=(0, 0, 1, 1),
                bold=True,
            ),
            style="text",
        )

        self.notEmptyDialogBox = MDDialog(
            MDDialogHeadlineText(text="ERROR"),
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

    def productDataValidationPopUpBox(self):
        # buttons for the popup field
        self.validationOkBtn = MDButton(
            MDButtonText(
                text="Ok",
                theme_text_color="Custom",
                text_color=(0, 0, 1, 1),
                bold=True,
            ),
            style="text",
        )

        self.validateDialogBox = MDDialog(
            MDDialogHeadlineText(text="ERROR"),
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

    # ============================ end of adding product to the database functionality===========================================

    # ====================editing the products in your database==================================

    def EditProductDialogPopUpBox(self):
        # buttons fof the popup field
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
            md_bg_color=(0, 0, 1, 1),
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
            md_bg_color=(0, 0, 1, 1),
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
            MDTextFieldHintText(text="product cost price", text_color_normal="gray"),
            text="",
        )
        self.editProductSpriceTextField = MDTextField(
            MDTextFieldHintText(text="product selling price", text_color_normal="gray"),
            text="",
        )
        self.editProductQuantityTextField = MDTextField(
            MDTextFieldHintText(text="product quantity", text_color_normal="gray"),
            text="",
        )

        self.editDialog = MDDialog(
            MDDialogHeadlineText(text="EDIT PRODUCT"),
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

    def openEditDialogPopUp(self):
        self.EditProductDialogPopUpBox().open()

    def searchProductToEdit(self, *args):
        productToSearch = (str(self.productToSearchInEditPopUp.text).strip()).lower()
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
                pass

    def confirmToEditProductDialogPopUpBox(self, instance, *args):
        # checking to make sure all the fields are not empty
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
                text_color=(0, 0, 1, 1),
                bold=True,
            ),
            style="text",
        )
        self.confirmEditDialogBox = MDDialog(
            MDDialogHeadlineText(text="EDIT PRODUCT"),
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
        except Exception as e:
            self.productDataValidationPopUpBox()

    def searchProductNotFoundPopupBox(self):
        # buttons for the popup field
        self.notFoundOkBtn = MDButton(
            MDButtonText(
                text="Ok",
                theme_text_color="Custom",
                text_color=(0, 0, 1, 1),
                bold=True,
            ),
            style="text",
        )

        self.notFoundDialogBox = MDDialog(
            MDDialogHeadlineText(text="ERROR"),
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

    # ====================end of editing the products in your database==================================

    # ================ deleating a product from the database=====================
    def deleteProductDialogBox(self):
        # buttons fof the popup field
        self.deleteProductNoBtn = MDButton(
            MDButtonText(
                text="close",
                theme_text_color="Custom",
                text_color=(0, 0, 1, 1),
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
                text="Enter product code or id", text_color_normal="gray"
            ),
            text="",
        )
        self.deleteDialog = MDDialog(
            MDDialogHeadlineText(text="DELETE PRODUCT"),
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
        self.deleteProductBtn.bind(on_press=self.confirmToDeleteProductDialogPopUpBox)
        self.deleteProductNoBtn.bind(on_press=self.deleteDialog.dismiss)
        return self.deleteDialog

    def openDeletePopuBox(self):
        self.deleteProductDialogBox().open()

    def deleteProductFromDatabase(self, *args):
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

    def confirmToDeleteProductDialogPopUpBox(self, instance, *args):
        # checking to make sure the search fields not empty
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
                text_color=(0, 0, 1, 1),
            ),
            style="text",
        )
        self.confirmDeleteDialogBox = MDDialog(
            MDDialogHeadlineText(text="DELETE PRODUCT"),
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

    def productToDeleteFieldsMustNotBeEmptyPopupBox(self):
        # buttons for the popup field
        self.delOkBtn = MDButton(
            MDButtonText(
                text="Ok",
                theme_text_color="Custom",
                text_color=(0, 0, 1, 1),
                bold=True,
            ),
            style="text",
        )

        self.notEmptyProductDialogBox = MDDialog(
            MDDialogHeadlineText(text="ERROR"),
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

    def productNoDeletedPopUp(self):
        # buttons for the popup field
        self.notDelededOkBtn = MDButton(
            MDButtonText(
                text="Ok",
                theme_text_color="Custom",
                text_color=(0, 0, 1, 1),
                bold=True,
            ),
            style="text",
        )

        self.notDelededDialogBox = MDDialog(
            MDDialogHeadlineText(text="ERROR"),
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

    # def allActionsConfirmationDialogBox(self, instance, *args):
    #     """this funtion is called any time you want to add,delet or edit a product.
    #     if if yes it then call the function that corespond to the approperite action such as
    #     1 addproduct()
    #     2 deleteproduct()
    #     3 comfirmEditProduct()
    #     """
    #     # buttons for the popup field
    #     self.NoBtn = MDButton(
    #         MDButtonText(text="No"),
    #         style="text",
    #     )
    #     self.yesBtn = MDButton(
    #         MDButtonText(text="yes"),
    #         style="text",
    #     )
    #     self.allActionsDialog = MDDialog(
    #         MDDialogHeadlineText(text=f"{instance}"),
    #         # this is where the text field for deleting the products is kept
    #         MDDialogSupportingText(
    #             text="Do you relly want to .",
    #             halign="left",
    #         ),
    #         MDDialogButtonContainer(
    #             MDWidget(),
    #             self.yesBtn,
    #             self.NoBtn,
    #             spacing="8dp",
    #         ),
    #         size_hint=(0.3, 0.5),
    #         auto_dismiss=False,
    #     )
    #     # binding buttons to perform setting actions when pressed in the dialog box
    #     self.yesBtn.bind(on_press=self.allActionConfirmBtn)
    #     self.NoBtn.bind(on_press=self.allActionsDialog.dismiss)
    #     return self.allActionsDialog.open()

    # def allActionConfirmBtn(self, instance):
    #     print(instance.text)
    #     pass
