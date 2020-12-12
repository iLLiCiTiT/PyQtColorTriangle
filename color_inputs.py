import re
from Qt import QtWidgets, QtCore, QtGui


slide_style = """
QSlider::groove:horizontal {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #000, stop: 1 #fff);
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ddd, stop:1 #bbb);
    border: 1px solid #777;
    width: 8px;
    margin-top: -1px;
    margin-bottom: -1px;
    border-radius: 4px;
}

QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eee, stop:1 #ddd);
    border: 1px solid #444;ff
    border-radius: 4px;
}"""


class AlphaInputs(QtWidgets.QGroupBox):
    alpha_changed = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(AlphaInputs, self).__init__("Alpha", parent)

        self._block_changes = False
        self.alpha_value = None

        # Opacity slider
        alpha_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        alpha_slider.setSingleStep(1)
        alpha_slider.setMinimum(0)
        alpha_slider.setMaximum(255)
        alpha_slider.setStyleSheet(slide_style)
        alpha_slider.setValue(255)

        inputs_widget = QtWidgets.QWidget(self)
        inputs_layout = QtWidgets.QHBoxLayout(inputs_widget)
        inputs_layout.setContentsMargins(0, 0, 0, 0)

        percent_input = QtWidgets.QDoubleSpinBox(self)
        percent_input.setMinimum(0)
        percent_input.setMaximum(100)
        percent_input.setDecimals(2)

        int_input = QtWidgets.QSpinBox(self)
        int_input.setMinimum(0)
        int_input.setMaximum(255)

        inputs_layout.addWidget(int_input)
        inputs_layout.addWidget(QtWidgets.QLabel("0-255"))
        inputs_layout.addWidget(percent_input)
        inputs_layout.addWidget(QtWidgets.QLabel("%"))

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(alpha_slider)
        layout.addWidget(inputs_widget)

        alpha_slider.valueChanged.connect(self._on_slider_change)
        percent_input.valueChanged.connect(self._on_percent_change)
        int_input.valueChanged.connect(self._on_int_change)

        self.alpha_slider = alpha_slider
        self.percent_input = percent_input
        self.int_input = int_input

        self.set_alpha(255)

    def set_alpha(self, alpha):
        if alpha == self.alpha_value:
            return
        self.alpha_value = alpha

        self.update_alpha()

    def _on_slider_change(self):
        if self._block_changes:
            return
        self.alpha_value = self.alpha_slider.value()
        self.alpha_changed.emit(self.alpha_value)
        self.update_alpha()

    def _on_percent_change(self):
        if self._block_changes:
            return
        self.alpha_value = int(self.percent_input.value() * 255 / 100)
        self.alpha_changed.emit(self.alpha_value)
        self.update_alpha()

    def _on_int_change(self):
        if self._block_changes:
            return

        self.alpha_value = self.int_input.value()
        self.alpha_changed.emit(self.alpha_value)
        self.update_alpha()

    def update_alpha(self):
        self._block_changes = True

        if self.alpha_slider.value() != self.alpha_value:
            self.alpha_slider.setValue(self.alpha_value)

        if self.int_input.value() != self.alpha_value:
            self.int_input.setValue(self.alpha_value)

        percent = round(100 * self.alpha_value / 255, 2)
        if self.percent_input.value() != percent:
            self.percent_input.setValue(percent)

        self._block_changes = False


class RGBInputs(QtWidgets.QGroupBox):
    value_changed = QtCore.Signal()

    def __init__(self, color, parent=None):
        super(RGBInputs, self).__init__("RGB", parent)

        self._block_changes = False

        self.color = color

        input_red = QtWidgets.QSpinBox(self)
        input_green = QtWidgets.QSpinBox(self)
        input_blue = QtWidgets.QSpinBox(self)

        input_red.setMinimum(0)
        input_green.setMinimum(0)
        input_blue.setMinimum(0)

        input_red.setMaximum(255)
        input_green.setMaximum(255)
        input_blue.setMaximum(255)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(input_red)
        layout.addWidget(input_green)
        layout.addWidget(input_blue)

        input_red.valueChanged.connect(self._on_red_change)
        input_green.valueChanged.connect(self._on_green_change)
        input_blue.valueChanged.connect(self._on_blue_change)

        self.input_red = input_red
        self.input_green = input_green
        self.input_blue = input_blue

    def _on_red_change(self, value):
        if self._block_changes:
            return
        self.color.setRed(value)
        self._on_change()

    def _on_green_change(self, value):
        if self._block_changes:
            return
        self.color.setGreen(value)
        self._on_change()

    def _on_blue_change(self, value):
        if self._block_changes:
            return
        self.color.setBlue(value)
        self._on_change()

    def _on_change(self):
        self.value_changed.emit()

    def color_changed(self):
        if (
            self.input_red.value() == self.color.red()
            and self.input_green.value() == self.color.green()
            and self.input_blue.value() == self.color.blue()
        ):
            return

        self._block_changes = True

        self.input_red.setValue(self.color.red())
        self.input_green.setValue(self.color.green())
        self.input_blue.setValue(self.color.blue())

        self._block_changes = False


class CMYKInputs(QtWidgets.QGroupBox):
    value_changed = QtCore.Signal()

    def __init__(self, color, parent=None):
        super(CMYKInputs, self).__init__("CMYK", parent)

        self.color = color

        self._block_changes = False

        input_cyan = QtWidgets.QSpinBox(self)
        input_magenta = QtWidgets.QSpinBox(self)
        input_yellow = QtWidgets.QSpinBox(self)
        input_black = QtWidgets.QSpinBox(self)

        input_cyan.setMinimum(0)
        input_magenta.setMinimum(0)
        input_yellow.setMinimum(0)
        input_black.setMinimum(0)

        input_cyan.setMaximum(255)
        input_magenta.setMaximum(255)
        input_yellow.setMaximum(255)
        input_black.setMaximum(255)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(input_cyan)
        layout.addWidget(input_magenta)
        layout.addWidget(input_yellow)
        layout.addWidget(input_black)

        input_cyan.valueChanged.connect(self._on_change)
        input_magenta.valueChanged.connect(self._on_change)
        input_yellow.valueChanged.connect(self._on_change)
        input_black.valueChanged.connect(self._on_change)

        self.input_cyan = input_cyan
        self.input_magenta = input_magenta
        self.input_yellow = input_yellow
        self.input_black = input_black

    def _on_change(self):
        if self._block_changes:
            return
        self.color.setCmyk(
            self.input_cyan.value(),
            self.input_magenta.value(),
            self.input_yellow.value(),
            self.input_black.value()
        )
        self.value_changed.emit()

    def color_changed(self):
        if self._block_changes:
            return
        _cur_color = QtGui.QColor()
        _cur_color.setCmyk(
            self.input_cyan.value(),
            self.input_magenta.value(),
            self.input_yellow.value(),
            self.input_black.value()
        )
        if (
            _cur_color.red() == self.color.red()
            and _cur_color.green() == self.color.green()
            and _cur_color.blue() == self.color.blue()
        ):
            return

        c, m, y, k, _ = self.color.getCmyk()
        self._block_changes = True

        self.input_cyan.setValue(c)
        self.input_magenta.setValue(m)
        self.input_yellow.setValue(y)
        self.input_black.setValue(k)

        self._block_changes = False


class HEXInputs(QtWidgets.QGroupBox):
    hex_regex = re.compile("^#(([0-9a-fA-F]{2}){3}|([0-9a-fA-F]){3})$")
    value_changed = QtCore.Signal()

    def __init__(self, color, parent=None):
        super(HEXInputs, self).__init__("HEX", parent)
        self.color = color

        input_field = QtWidgets.QLineEdit()

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(input_field)

        input_field.textChanged.connect(self._on_change)

        self.input_field = input_field

    def _on_change(self):
        if self._block_changes:
            return
        input_value = self.input_field.text()
        # TODO what if does not match?
        if self.hex_regex.match(input_value):
            self.color.setNamedColor(input_value)
            self.value_changed.emit()

    def color_changed(self):
        input_value = self.input_field.text()
        if self.hex_regex.match(input_value):
            _cur_color = QtGui.QColor()
            _cur_color.setNamedColor(input_value)
            if (
                _cur_color.red() == self.color.red()
                and _cur_color.green() == self.color.green()
                and _cur_color.blue() == self.color.blue()
            ):
                return
        self._block_changes = True

        self.input_field.setText(self.color.name())

        self._block_changes = False


class HSVInputs(QtWidgets.QGroupBox):
    value_changed = QtCore.Signal()

    def __init__(self, color, parent=None):
        super(HSVInputs, self).__init__("HSV", parent)

        self._block_changes = False

        self.color = color

        input_hue = QtWidgets.QSpinBox(self)
        input_sat = QtWidgets.QSpinBox(self)
        input_val = QtWidgets.QSpinBox(self)

        input_hue.setMinimum(0)
        input_sat.setMinimum(0)
        input_val.setMinimum(0)

        input_hue.setMaximum(359)
        input_sat.setMaximum(255)
        input_val.setMaximum(255)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(input_hue)
        layout.addWidget(input_sat)
        layout.addWidget(input_val)

        input_hue.valueChanged.connect(self._on_change)
        input_sat.valueChanged.connect(self._on_change)
        input_val.valueChanged.connect(self._on_change)

        self.input_hue = input_hue
        self.input_sat = input_sat
        self.input_val = input_val

    def _on_change(self):
        if self._block_changes:
            return
        self.color.setHsv(
            self.input_hue.value(),
            self.input_sat.value(),
            self.input_val.value()
        )
        self.value_changed.emit()

    def color_changed(self):
        _cur_color = QtGui.QColor()
        _cur_color.setHsv(
            self.input_hue.value(),
            self.input_sat.value(),
            self.input_val.value()
        )
        if (
            _cur_color.red() == self.color.red()
            and _cur_color.green() == self.color.green()
            and _cur_color.blue() == self.color.blue()
        ):
            return

        self._block_changes = True
        h, s, v, _ = self.color.getHsv()

        self.input_hue.setValue(h)
        self.input_sat.setValue(s)
        self.input_val.setValue(v)

        self._block_changes = False


class HSLInputs(QtWidgets.QGroupBox):
    value_changed = QtCore.Signal()

    def __init__(self, color, parent=None):
        super(HSLInputs, self).__init__("HSL", parent)

        self._block_changes = False

        self.color = color

        input_hue = QtWidgets.QSpinBox(self)
        input_sat = QtWidgets.QSpinBox(self)
        input_light = QtWidgets.QSpinBox(self)

        input_hue.setMinimum(0)
        input_sat.setMinimum(0)
        input_light.setMinimum(0)

        input_hue.setMaximum(359)
        input_sat.setMaximum(255)
        input_light.setMaximum(255)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(input_hue)
        layout.addWidget(input_sat)
        layout.addWidget(input_light)

        input_hue.valueChanged.connect(self._on_change)
        input_sat.valueChanged.connect(self._on_change)
        input_light.valueChanged.connect(self._on_change)

        self.input_hue = input_hue
        self.input_sat = input_sat
        self.input_light = input_light

    def _on_change(self):
        if self._block_changes:
            return
        self.color.setHsl(
            self.input_hue.value(),
            self.input_sat.value(),
            self.input_light.value()
        )
        self.value_changed.emit()

    def color_changed(self):
        _cur_color = QtGui.QColor()
        _cur_color.setHsl(
            self.input_hue.value(),
            self.input_sat.value(),
            self.input_light.value()
        )
        if (
            _cur_color.red() == self.color.red()
            and _cur_color.green() == self.color.green()
            and _cur_color.blue() == self.color.blue()
        ):
            return

        self._block_changes = True
        h, s, l, _ = self.color.getHsl()

        self.input_hue.setValue(h)
        self.input_sat.setValue(s)
        self.input_light.setValue(l)

        self._block_changes = False


class ColorInputsWidget(QtWidgets.QWidget):
    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self, parent=None):
        super(ColorInputsWidget, self).__init__(parent)

        color = QtGui.QColor()

        hex_input = HEXInputs(color, self)
        rgb_input = RGBInputs(color, self)
        hsl_input = HSLInputs(color, self)
        hsv_input = HSVInputs(color, self)
        cmyk_input = CMYKInputs(color, self)

        input_fields = [
            hex_input,
            rgb_input,
            hsl_input,
            hsv_input,
            cmyk_input
        ]

        inputs_widget = QtWidgets.QWidget(self)
        inputs_layout = QtWidgets.QVBoxLayout(inputs_widget)

        for input_field in input_fields:
            inputs_layout.addWidget(input_field)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(inputs_widget, 0)
        spacer = QtWidgets.QWidget(self)
        layout.addWidget(spacer, 1)

        hex_input.value_changed.connect(self._on_value_change)
        rgb_input.value_changed.connect(self._on_value_change)
        cmyk_input.value_changed.connect(self._on_value_change)
        hsl_input.value_changed.connect(self._on_value_change)
        hsv_input.value_changed.connect(self._on_value_change)

        self.input_fields = input_fields

        self.hex_input = hex_input
        self.rgb_input = rgb_input
        self.hsl_input = hsl_input
        self.hsv_input = hsv_input
        self.cmyk_input = cmyk_input

        self.color = color

    def set_color(self, color):
        if (
            color.red() == self.color.red()
            and color.green() == self.color.green()
            and color.blue() == self.color.blue()
        ):
            return
        self.color.setRed(color.red())
        self.color.setGreen(color.green())
        self.color.setBlue(color.blue())
        self._on_value_change()

    def _on_value_change(self):
        for input_field in self.input_fields:
            input_field.color_changed()
        self.color_changed.emit(self.color)
