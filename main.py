from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import sys

def resource_path(relative_path):
    import sys
    import os

    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    if IsWindows():
        return os.path.join(base_path, relative_path).replace("/", "\\")
    else:
        return os.path.join(base_path, relative_path)


def IsBundled():
    import sys

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return True
    else:
        return False


def IsWindows():
    import sys

    if hasattr(sys, "getwindowsversion"):
        return True
    else:
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.MovementLocked = False

        self.Toolbars = []

        self.setMinimumSize(QSize(800, 600))
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.Toolbars.append(toolbar)
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addToolBar(toolbar)

        QuitButton = QAction("Quit", self)
        QuitButton.setIcon(QIcon(resource_path('img/icons/circle-x.svg')))
        QuitButton.triggered.connect(lambda: self.close())

        NewButton = QAction("New File", self)
        NewButton.setIcon(QIcon(resource_path('img/icons/file-plus.svg')))

        OpenButton = QAction("Open File", self)
        OpenButton.setIcon(QIcon(resource_path('img/icons/folder-open.svg')))
        toolbar.addAction(OpenButton)

        SaveButton = QAction("Save File", self)
        SaveButton.setIcon(QIcon(resource_path('img/icons/save.svg')))

        CutButton = QAction("Cut", self)
        CutButton.setIcon(QIcon(resource_path('img/icons/scissors.svg')))
        CutButton.triggered.connect(self.Cut)

        CopyButton = QAction("Copy", self)
        CopyButton.setIcon(QIcon(resource_path('img/icons/clipboard-copy.svg')))
        CopyButton.triggered.connect(self.Copy)

        PasteButton = QAction("Paste", self)
        PasteButton.setIcon(QIcon(resource_path('img/icons/clipboard-paste.svg')))
        PasteButton.triggered.connect(self.Paste)

        UndoButton = QAction("Undo", self)
        UndoButton.setIcon(QIcon(resource_path('img/icons/undo.svg')))
        UndoButton.triggered.connect(self.Undo)
        toolbar.addAction(UndoButton)

        toolbar.insertSeparator(UndoButton)

        RedoButton = QAction("Redo", self)
        RedoButton.setIcon(QIcon(resource_path('img/icons/redo.svg')))
        RedoButton.triggered.connect(self.Redo)
        toolbar.addAction(RedoButton)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        self.MenuButton = QAction("Menu", self)
        self.MenuButton.setIcon(QIcon(resource_path('img/icons/panel-right-close.svg')))
        self.MenuButton.triggered.connect(self.ShowHideSidebar)
        toolbar.addAction(self.MenuButton)

        #Editor
        mainlayout = QHBoxLayout()
        layout.addLayout(mainlayout)

        #Input Editor
        self.input_editor = QTextEdit(self,
            placeholderText = "Type something here",
            lineWrapColumnOrWidth = 100,
            readOnly = False,
            acceptRichText = False)
        self.input_editor.setContextMenuPolicy(Qt.NoContextMenu)
        mainlayout.addWidget(self.input_editor)

        #Output Editor
        self.output_editor = QTextEdit(self,
            lineWrapColumnOrWidth = 100,
            readOnly = True,
            acceptRichText = False
        )
        self.output_editor.setContextMenuPolicy(Qt.NoContextMenu)
        mainlayout.addWidget(self.output_editor)
        self.output_editor.setObjectName('Output')

        #Live Preview
        self.input_editor.textChanged.connect(self.on_input_change)

        self.SideBar = QWidget()
        self.SideLayout = QVBoxLayout()

        self.SideBar.setLayout(self.SideLayout)

        mainlayout.addWidget(self.SideBar)

        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addAction(NewButton)
        file_menu.addAction(OpenButton)
        file_menu.addAction(SaveButton)
        file_menu.insertSeparator(QuitButton)
        file_menu.addAction(QuitButton)

        edit_menu = menu.addMenu("Edit")
        edit_menu.addAction(CutButton)
        edit_menu.addAction(CopyButton)
        edit_menu.addAction(PasteButton)
        edit_menu.addAction(UndoButton)
        edit_menu.insertSeparator(UndoButton)
        edit_menu.addAction(RedoButton)

    def Cut(self):
        self.input_editor.cut()

    def Copy(self):
        self.input_editor.copy()
    
    def Paste(self):
        self.input_editor.Paste()

    def Undo(self):
        self.input_editor.undo()

    def Redo(self):
        self.input_editor.redo()

    #Live Preview
    def on_input_change(self):
        self.output_editor.setMarkdown(self.input_editor.toPlainText())

    #Preview 
    def preview_panel(self):
        if not self.preview_hidden:
            self.output_editor.hide()
            self.preview_hidden = True
            self.preview.setToolTip("Show Preview")
            self.preview.setIcon(QIcon('Icons/Preview_Open.png'))
        else:
            self.output_editor.show()
            self.preview_hidden = False
            self.preview.setToolTip("Close Preview")
            self.preview.setIcon(QIcon('Icons/Preview_Close.png'))

    #Handle Sidebar

    def ShowHideSidebar(self):
        if self.SideBar.isHidden():
            self.MenuButton.setIcon(
                QIcon(resource_path('img/icons/panel-right-close.svg'))
            )
            self.SideBar.setHidden(False)
        else:
            self.MenuButton.setIcon(
                QIcon(resource_path('img/icons/panel-right-open.svg'))
            )
            self.SideBar.setHidden(True)

    #HandleToolbars
    def LockToolbars(self):
        self.MovementLocked = not self.MovementLocked

        if self.MovementLocked:
            for i in self.Toolbars:
                i.setMovable(False)
        else:
            for i in self.Toolbars:
                i.setMovable(True)

if __name__ == '__main__':
    #Initialize the App
    app = QApplication(sys.argv)
    app.setApplicationName("Blocketh")

    window = MainWindow()

    window.show()
    app.exec_()