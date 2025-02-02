from __future__ import annotations

from typing import TYPE_CHECKING, Mapping
import weakref

from qtpy import QtWidgets as QtW, QtCore, QtGui

from himena_builtins.qt.widgets._table_components._selection_model import Index
from himena.standards.model_meta import ExcelMeta
from himena.qt._qrename import QTabRenameLineEdit
from himena.qt import drag_model
from himena_builtins.qt.widgets.table import QSpreadsheet
from himena_builtins.qt.widgets._table_components import QSelectionRangeEdit
from himena.types import DragDataModel, DropResult, WidgetDataModel
from himena.consts import StandardType
from himena.plugins import validate_protocol

if TYPE_CHECKING:
    import numpy as np

_EDIT_DISABLED = QtW.QAbstractItemView.EditTrigger.NoEditTriggers
_EDIT_ENABLED = (
    QtW.QAbstractItemView.EditTrigger.DoubleClicked
    | QtW.QAbstractItemView.EditTrigger.EditKeyPressed
)


class QRightClickableTabBar(QtW.QTabBar):
    right_clicked = QtCore.Signal(int)

    def __init__(self, parent: QExcelEdit) -> None:
        super().__init__(parent)
        self._last_right_clicked = None
        self._is_dragging = False
        self._excel_ref = weakref.ref(parent)

    def mousePressEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        if a0 is not None and a0.button() == QtCore.Qt.MouseButton.RightButton:
            self._last_right_clicked = self.tabAt(a0.pos())
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0):
        if self._is_dragging:
            return super().mouseMoveEvent(a0)
        self._is_dragging = True
        if (
            a0.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier
            and a0.buttons() & QtCore.Qt.MouseButton.LeftButton
        ) or QtCore.Qt.MouseButton.MiddleButton:
            if (qexcel := self._excel_ref()) and (widget := qexcel.currentWidget()):
                tab_text = qexcel.tabText(qexcel.currentIndex())

                def _getter():
                    model = widget.to_model()
                    model.title = tab_text
                    return model

                drag_model(
                    DragDataModel(getter=_getter, type=StandardType.TABLE),
                    desc=tab_text,
                    source=qexcel,
                )

        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent | None) -> None:
        if a0 is not None and a0.button() == QtCore.Qt.MouseButton.RightButton:
            if self.tabAt(a0.pos()) == self._last_right_clicked:
                self.right_clicked.emit(self._last_right_clicked)
        self._last_right_clicked = None
        self._is_dragging = False
        return super().mouseReleaseEvent(a0)


class QExcelEdit(QtW.QTabWidget):
    """Built-in Excel File Editor.

    ## Basic Usage

    This widget is used to view and edit Excel books (stack of spreadsheets). It works
    almost like a tabbed list of built-in spreadsheet for simple table types. Note that
    this widget is not designed for full replacement of Excel software. Rich text,
    formulas, and other advanced features are not supported.

    ## Drag and Drop

    Dragging a tab will provide a model of type `StandardType.TABLE` ("table").
    `Ctrl + left_button` or `middle button` are assigned to the drag event.
    """

    __himena_widget_id__ = "builtins:QExcelEdit"
    __himena_display_name__ = "Built-in Excel File Editor"

    def __init__(self):
        super().__init__()
        self.setTabBar(QRightClickableTabBar(self))
        self._edit_trigger = _EDIT_ENABLED
        self._control = QExcelTableStackControl()
        self.currentChanged.connect(self._on_tab_changed)
        self._line_edit = QTabRenameLineEdit(self, allow_duplicate=False)

        # corner widget for adding new tab
        tb = QtW.QToolButton()
        tb.setText("+")
        tb.setFont(QtGui.QFont("Arial", 12, weight=15))
        tb.setToolTip("New Tab")
        tb.clicked.connect(self.add_new_tab)
        self.setCornerWidget(tb, QtCore.Qt.Corner.TopRightCorner)
        self.tabBar().right_clicked.connect(self._tabbar_right_clicked)
        self._model_type = StandardType.EXCEL

    def _on_tab_changed(self, index: int):
        self._control.update_for_table(self.widget(index))
        return None

    def _tabbar_right_clicked(self, index: int):
        if index < 0:  # Clicked on the empty space
            return
        else:  # Clicked on an existing tab
            menu = QtW.QMenu(self)
            rename_action = menu.addAction("Rename Tab")
            delete_action = menu.addAction("Delete Tab")
            action = menu.exec_(QtGui.QCursor.pos())
            if action == rename_action:
                self._line_edit.start_edit(index)
            elif action == delete_action:
                self.removeTab(index)

    def add_new_tab(self):
        table = QSpreadsheet()
        table.update_model(WidgetDataModel(value=None, type=StandardType.TABLE))
        table.setHeaderFormat(QSpreadsheet.HeaderFormat.Alphabetic)
        self.addTab(table, f"Sheet-{self.count() + 1}")
        self.setCurrentIndex(self.count() - 1)
        self._control.update_for_table(table)
        return None

    @validate_protocol
    def update_model(self, model: WidgetDataModel):
        if not isinstance(value := model.value, Mapping):
            raise ValueError(f"Expected a dict, got {type(value)}")
        self.clear()
        for sheet_name, each in value.items():
            table = QSpreadsheet()
            table.update_model(WidgetDataModel(value=each, type=StandardType.TABLE))
            table.setHeaderFormat(QSpreadsheet.HeaderFormat.Alphabetic)
            self.addTab(table, str(sheet_name))
        if self.count() > 0:
            self.setCurrentIndex(0)
            self._control.update_for_table(self.widget(0))
        self._model_type = model.type
        return None

    @validate_protocol
    def to_model(self) -> WidgetDataModel[dict[str, np.ndarray]]:
        index = self.currentIndex()
        table_meta = self.widget(index)._prep_table_meta()
        return WidgetDataModel(
            value={
                self.tabText(i): self.widget(i).to_model().value
                for i in range(self.count())
            },
            type=self.model_type(),
            extension_default=".xlsx",
            metadata=ExcelMeta(
                current_position=table_meta.current_position,
                selections=table_meta.selections,
                current_sheet=self.tabText(index),
            ),
        )

    @validate_protocol
    def control_widget(self) -> QExcelTableStackControl:
        return self._control

    @validate_protocol
    def model_type(self):
        return self._model_type

    @validate_protocol
    def is_modified(self) -> bool:
        return any(self.widget(i).is_modified() for i in range(self.count()))

    @validate_protocol
    def set_modified(self, value: bool) -> None:
        for i in range(self.count()):
            self.widget(i).set_modified(value)

    @validate_protocol
    def size_hint(self) -> tuple[int, int]:
        return 400, 300

    @validate_protocol
    def is_editable(self) -> bool:
        return self._edit_trigger == _EDIT_ENABLED

    @validate_protocol
    def set_editable(self, value: bool) -> None:
        self._edit_trigger = _EDIT_ENABLED if value else _EDIT_DISABLED
        for i in range(self.count()):
            self.widget(i).set_editable(value)

    @validate_protocol
    def allowed_drop_types(self) -> list[str]:
        return [StandardType.EXCEL, StandardType.TABLE]

    @validate_protocol
    def dropped_callback(self, model: WidgetDataModel) -> DropResult:
        if model.type == StandardType.EXCEL:  # merge all the sheets
            assert isinstance(model.value, dict)
            for key, value in model.value.items():
                table = QSpreadsheet()
                table.setHeaderFormat(QSpreadsheet.HeaderFormat.Alphabetic)
                table.update_model(
                    WidgetDataModel(value=value, type=StandardType.TABLE)
                )
                self.addTab(table, key)
        elif model.type == StandardType.TABLE:  # merge as a new sheet
            table = QSpreadsheet()
            table.setHeaderFormat(QSpreadsheet.HeaderFormat.Alphabetic)
            table.update_model(model)
            self.addTab(table, model.title)
        else:
            raise ValueError(f"Cannot merge {model.type} with {StandardType.EXCEL}")
        return DropResult(delete_input=True)

    if TYPE_CHECKING:

        def widget(self, index: int) -> QSpreadsheet: ...
        def currentWidget(self) -> QSpreadsheet: ...
        def tabBar(self) -> QRightClickableTabBar: ...


_R_CENTER = QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter


class QExcelTableStackControl(QtW.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtW.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(_R_CENTER)
        # self._header_format = QtW.QComboBox()
        # self._header_format.addItems(["0, 1, 2, ...", "1, 2, 3, ...", "A, B, C, ..."])
        self._value_line_edit = QtW.QLineEdit()
        self._label = QtW.QLabel("")
        self._label.setAlignment(_R_CENTER)
        self._selection_range = QSelectionRangeEdit()
        # layout.addWidget(self._header_format)

        # toolbuttons
        self._insert_menu_button = QtW.QPushButton()
        self._insert_menu_button.setText("Ins")  # or "icons8:plus"
        self._insert_menu_button.setMenu(self._make_insert_menu())
        self._remove_menu_button = QtW.QPushButton()
        self._remove_menu_button.setText("Rem")
        self._remove_menu_button.setMenu(self._make_delete_menu())

        layout.addWidget(self._value_line_edit)
        layout.addWidget(self._insert_menu_button)
        layout.addWidget(self._remove_menu_button)
        layout.addWidget(self._label)
        layout.addWidget(self._selection_range)
        self._value_line_edit.editingFinished.connect(self.update_for_editing)

    def update_for_table(self, table: QSpreadsheet | None):
        if table is None:
            return
        shape = table.model()._arr.shape
        self._label.setText(f"Shape {shape!r}")
        self._selection_range.connect_table(table)
        table._selection_model.moved.connect(self.update_for_current_index)
        self.update_for_current_index(
            table._selection_model.current_index, table._selection_model.current_index
        )
        return None

    @property
    def _current_table(self) -> QSpreadsheet | None:
        return self._selection_range._qtable

    def update_for_current_index(self, old: Index, new: Index):
        qtable = self._current_table
        if qtable is None:
            return None
        qindex = qtable.model().index(new.row, new.column)
        text = qtable.model().data(qindex)
        if not isinstance(text, str):
            text = ""
        self._value_line_edit.setText(text)
        return None

    def update_for_editing(self):
        qtable = self._current_table
        if qtable is None:
            return None
        text = self._value_line_edit.text()
        index = qtable._selection_model.current_index
        qindex = qtable.model().index(index.row, index.column)
        qtable.model().setData(qindex, text, QtCore.Qt.ItemDataRole.EditRole)
        qtable.setFocus()
        return None

    def _make_insert_menu(self):
        menu = QtW.QMenu(self)
        menu.addAction("Row above", self._insert_row_above)
        menu.addAction("Row below", self._insert_row_below)
        menu.addAction("Column left", self._insert_column_left)
        menu.addAction("Column right", self._insert_column_right)
        return menu

    def _make_delete_menu(self):
        menu = QtW.QMenu(self)
        menu.addAction("Rows", self._remove_selected_rows)
        menu.addAction("Columns", self._remove_selected_columns)
        return menu

    def _insert_row_above(self):
        if qtable := self._current_table:
            qtable._insert_row_above()
        return None

    def _insert_row_below(self):
        if qtable := self._current_table:
            qtable._insert_row_below()
        return None

    def _insert_column_left(self):
        if qtable := self._current_table:
            qtable._insert_column_left()
        return None

    def _insert_column_right(self):
        if qtable := self._current_table:
            qtable._insert_column_right()
        return None

    def _remove_selected_rows(self):
        if qtable := self._current_table:
            qtable._remove_selected_rows()
        return None

    def _remove_selected_columns(self):
        if qtable := self._current_table:
            qtable._remove_selected_columns()
        return None
