from PyQt5.QtWidgets import QWidget, QPushButton
from ..pie_style import PieStyle
from api_krita.pyqt import MovableWidget
from api_krita import Krita


class AcceptButton(QPushButton, MovableWidget):
    def __init__(self, style: PieStyle, parent: QWidget):
        QPushButton.__init__(self, Krita.get_icon("dialog-ok"), "", parent)

        self._style = style
        self.hide()
        self.radius = round(self._style.deadzone_radius*0.9)
        self.setGeometry(
            0, 0,
            self.radius*2,
            self.radius*2)

        color_1 = "rgba(50, 120, 50)"
        color_2 = "rgba(70, 150, 70)"
        color_3 = "rgba(90, 170, 90)"
        color_4 = "rgba(120, 200, 120)"
        self.setStyleSheet(
            f"""QPushButton [
                color: #333;
                border:{self._style.border_thickness}px {color_1};
                border-radius: {self.radius}px;
                border-style: outset;
                background: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 {color_4}, stop: 1 {color_2}
                );
                padding: 5px;
                qproperty-iconSize:{round(self.radius*1.5)}px;
            ]
            QPushButton:hover [
                background: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 {color_4}, stop: 1 {color_3}
                )
            ]
        """.replace('[', '{').replace(']', '}')
        )
