from kivy.uix.accordion import BooleanProperty
from kivy.uix.actionbar import Label
from View.base_screen import BaseScreen
from kivy.properties import ObjectProperty

# for the recycle view behaview
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


class AdminScreenView(BaseScreen):
    products_data = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.products_data = self.ids.products_data


class SelectableRecycleBoxLayout(
    FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout
): ...  # add selection and focus behavior to the view


class SelectableLabel(RecycleDataViewBehavior, Label, AdminScreenView):
    # adds selection supprort to the lable
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        # catches and handle the view changes
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        # add selection on touch down
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        # respond to the selection of itermsion in the view
        self.selected = is_selected
        # this is use to determine which sales data to display base on the selected data
        if is_selected:
            # displaying all the sales
            if str(rv.data[index]["text"]).lower() == "all sales":
                print(str(rv.data[index]["text"]).lower())
            print("selection change to {0}".format(rv.data[index]))
        # else:
        #     print("selection remove from for {0}".format(rv.data[index]))


class FilterRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(FilterRecycleView, self).__init__(**kwargs)
        # self.data = [{"text": str(x)} for x in range(100)]
