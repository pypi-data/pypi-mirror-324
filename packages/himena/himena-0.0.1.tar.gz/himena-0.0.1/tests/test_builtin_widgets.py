from himena.widgets import MainWindow
from himena_builtins.qt.history._widget import QCommandHistory

def test_command_added(himena_ui: MainWindow):
    history_widget = QCommandHistory(himena_ui)
    assert history_widget._command_list.model().rowCount() == 0
    himena_ui.exec_action("new-tab")
    assert history_widget._command_list.model().rowCount() == 1
    himena_ui.exec_action("builtins:new-text")
