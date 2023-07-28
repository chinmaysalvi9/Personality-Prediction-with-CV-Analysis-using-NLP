from PyQt5.QtWidgets import QDesktopWidget


def center_window(ui_object):
    geo = ui_object.frameGeometry()
    geo.moveCenter(QDesktopWidget().availableGeometry().center())
    ui_object.move((geo.topLeft()))
