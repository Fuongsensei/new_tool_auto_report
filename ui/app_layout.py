import ctypes
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QPoint

# DWM Consts
DWMWA_SYSTEMBACKDROP_TYPE = 38
DWMSBT_MAINWINDOW = 2 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Report Tool")
        self.resize(1000, 700)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self._setup_acrylic()
        
        # UI Setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Dùng QHBoxLayout để chia NAV (trái) và Content (phải)
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.nav = QFrame()
        self.nav.setFixedWidth(250)
        self.nav.setObjectName("nav_bar")
        self.layout.addWidget(self.nav)

        self.main_content = QFrame()
        self.main_content.setObjectName("content_area")
        self.layout.addWidget(self.main_content)

        # Style
        self.setStyleSheet("""
            #nav_bar {
                background-color: rgba(30, 30, 30, 150);
                border-right: 1px solid rgba(255, 255, 255, 30);
            }
            #content_area {
                background-color: rgba(40, 40, 40, 100);
            }
        """)

        # Dragging logic (frameless window)
        self.oldPos = QPoint()

    def _setup_acrylic(self):
        hwnd = int(self.winId())
        backdrop_type = ctypes.c_int(DWMSBT_MAINWINDOW)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_SYSTEMBACKDROP_TYPE, ctypes.byref(backdrop_type), ctypes.sizeof(backdrop_type)
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPosition().toPoint()