from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QWidget


class Label:
    def __init__(
        self,
        widget: QWidget,
        center: QPoint,
        size: int,
        text: str,
        bg_color: QColor = QColor(47, 47, 47, 255)
    ):
        self.label = QLabel("text label", widget)
        self.label.setFont(QFont('Times', 20))
        self.label.adjustSize()
        self.label.setGeometry(
            round(center.x()-size//2),
            round(center.y()-size//2),
            size,
            size
        )
        self.label.setStyleSheet(
            f"""background-color:rgba(
                {bg_color.red()},
                {bg_color.green()},
                {bg_color.blue()},
                {bg_color.alpha()}
            );"""
            "color: white;"
        )
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setText(text)

        self.label.show()
