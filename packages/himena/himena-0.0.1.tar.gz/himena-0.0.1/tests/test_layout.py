from himena import MainWindow
from himena.types import Margins
from himena.layout import EmptyLayout
from magicgui import widgets as mgw
from qtpy.QtWidgets import QApplication

def test_layout_1d(himena_ui: MainWindow):
    tab = himena_ui.add_tab()
    vlayout = tab.add_vbox_layout(margins=(2, 2, 3, 2))
    win0 = tab.add_widget(mgw.Label(value="label 0"))
    win1 = tab.add_widget(mgw.Label(value="label 1"))
    win2 = tab.add_widget(mgw.Label(value="label 2"))
    vlayout.add(win0)
    hlayout = vlayout.add_hbox_layout(spacing=3)
    hlayout.add(win1, win2, EmptyLayout())
    assert vlayout.margins == Margins(2, 2, 3, 2)
    assert vlayout.spacing == 0
    assert hlayout.margins == Margins(0, 0, 0, 0)
    assert hlayout.spacing == 3
    himena_ui.size = (500, 500)
    QApplication.processEvents()
    himena_ui.size = (600, 400)
    QApplication.processEvents()

    del hlayout[1]
    hlayout.spacing = 10
    hlayout.set_margins(left=1)
    himena_ui.size = (500, 500)
    QApplication.processEvents()
    himena_ui.size = (600, 400)
    QApplication.processEvents()
    win0.size = win0.size.with_height(win0.rect.height + 5)
    QApplication.processEvents()
    win0.size = win0.size.with_height(win0.rect.height - 5)
    QApplication.processEvents()
    win2.size = win2.size.with_height(win0.rect.width + 5)
    QApplication.processEvents()
    win2.size = win2.size.with_height(win0.rect.width - 5)
    QApplication.processEvents()
