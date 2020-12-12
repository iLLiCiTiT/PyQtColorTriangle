import sys
from Qt import QtWidgets
from color_picker_widget import ColorPickerWidget


class ExampleDialog(QtWidgets.QDialog):
    def __init__(self, color=None, parent=None):
        super(ExampleDialog, self).__init__(parent)

        picker_widget = ColorPickerWidget()

        footer_widget = QtWidgets.QWidget(self)
        footer_layout = QtWidgets.QHBoxLayout(footer_widget)

        ok_btn = QtWidgets.QPushButton("Ok", footer_widget)
        cancel_btn = QtWidgets.QPushButton("Cancel", footer_widget)

        footer_layout.addWidget(ok_btn)
        footer_layout.addWidget(cancel_btn)
        footer_layout.addWidget(QtWidgets.QWidget(self), 1)

        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(picker_widget, 1)
        layout.addWidget(footer_widget, 0)

        ok_btn.clicked.connect(self.on_ok_clicked)
        cancel_btn.clicked.connect(self.on_cancel_clicked)

        self.picker_widget = picker_widget

        self._result = None

    def on_ok_clicked(self):
        self._result = self.picker_widget.color()
        self.close()

    def on_cancel_clicked(self):
        self._result = None
        self.close()

    def result(self):
        return self._result


class ExampleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ExampleWidget, self).__init__(parent)

        btn_example = QtWidgets.QPushButton("Start", self)
        output_label = QtWidgets.QLabel("None", self)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(btn_example)
        layout.addWidget(output_label)

        btn_example.clicked.connect(self.on_example)

        self.output_label = output_label

    def on_example(self):
        dialog = ExampleDialog()
        dialog.exec_()

        color = dialog.result()
        if color:
            self.output_label.setText("R: {}\nG: {}\nB: {}\nA: {}".format(
                color.red(), color.green(), color.blue(), color.alpha()
            ))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleWidget()
    window.show()
    sys.exit(app.exec())
