from Qt import QtWidgets, QtCore, QtGui

from color_triangle import QtColorTriangle
from color_view import ColorViewer
from color_screen_pick import PickScreenColorWidget
from color_inputs import (
    ColorInputsWidget,
    AlphaInputs
)


class ColorPickerWidget(QtWidgets.QWidget):
    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self, parent=None):
        super(ColorPickerWidget, self).__init__(parent)

        # Eye picked widget
        pick_widget = PickScreenColorWidget()

        # Color utils
        utils_widget = QtWidgets.QWidget(self)
        utils_layout = QtWidgets.QVBoxLayout(utils_widget)

        bottom_utils_widget = QtWidgets.QWidget(utils_widget)

        # Color triangle
        color_triangle = QtColorTriangle(utils_widget)

        # Color preview
        color_view = ColorViewer(bottom_utils_widget)
        color_view.setMaximumHeight(50)

        # Color pick button
        btn_pick_color = QtWidgets.QPushButton(
            "Pick a color", bottom_utils_widget
        )

        # Color inputs widget
        color_inputs = ColorInputsWidget(self)

        # Alpha inputs
        alpha_input_wrapper_widget = QtWidgets.QWidget(self)
        alpha_input_wrapper_layout = QtWidgets.QVBoxLayout(
            alpha_input_wrapper_widget
        )

        alpha_inputs = AlphaInputs(alpha_input_wrapper_widget)
        alpha_input_wrapper_layout.addWidget(alpha_inputs)
        alpha_input_wrapper_layout.addWidget(QtWidgets.QWidget(), 1)

        bottom_utils_layout = QtWidgets.QHBoxLayout(bottom_utils_widget)
        bottom_utils_layout.setContentsMargins(0, 0, 0, 0)
        bottom_utils_layout.addWidget(color_view, 1)
        bottom_utils_layout.addWidget(btn_pick_color, 0)

        utils_layout.addWidget(bottom_utils_widget, 0)
        utils_layout.addWidget(color_triangle, 1)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(utils_widget, 1)
        layout.addWidget(color_inputs, 0)
        layout.addWidget(alpha_input_wrapper_widget, 0)

        color_view.set_color(color_triangle.cur_color)
        color_inputs.set_color(color_triangle.cur_color)

        color_triangle.color_changed.connect(self.triangle_color_changed)
        pick_widget.color_selected.connect(self.on_color_change)
        color_inputs.color_changed.connect(self.on_color_change)
        alpha_inputs.alpha_changed.connect(self.alpha_changed)
        btn_pick_color.released.connect(self.pick_color)

        self.pick_widget = pick_widget
        self.utils_widget = utils_widget
        self.bottom_utils_widget = bottom_utils_widget

        self.color_triangle = color_triangle
        self.color_view = color_view
        self.btn_pick_color = btn_pick_color
        self.color_inputs = color_inputs
        self.alpha_inputs = alpha_inputs

    def show(self):
        super(ColorPickerWidget, self).show()
        triangle_width = (
            self.utils_widget.height() - self.bottom_utils_widget.height()
        )
        width = (
            triangle_width
            + self.color_inputs.width()
            + self.alpha_inputs.width()
        )
        self.resize(width, self.height())

    def setColor(self, color):
        self.alpha_inputs.set_alpha(color.alpha())
        self.on_color_change(color)

    def pick_color(self):
        self.pick_widget.pick_color()

    def triangle_color_changed(self, color):
        self.color_view.set_color(color)
        self.color_inputs.set_color(color)

    def on_color_change(self, color):
        self.color_view.set_color(color)
        self.color_triangle.set_color(color)
        self.color_inputs.set_color(color)

    def alpha_changed(self, alpha):
        self.color_view.set_alpha(alpha)
