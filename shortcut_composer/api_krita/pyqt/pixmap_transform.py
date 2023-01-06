from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QBrush,
)


def add_border(pixmap: QPixmap, border_part: float = 0.33):
    original_size = pixmap.width()
    border_size = round(original_size * border_part)
    new_size = original_size + 2*border_size

    result = QPixmap(new_size, new_size)
    result.fill(Qt.transparent)
    painter = QPainter(result)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
    painter.drawPixmap(QPoint(), result)
    painter.drawPixmap(border_size, border_size, pixmap)
    painter.end()
    return result


def make_pixmap_round(pixmap: QPixmap) -> QPixmap:
    image = pixmap.toImage()
    image.convertToFormat(QImage.Format_ARGB32)

    imgsize = min(image.width(), image.height())
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    painter = QPainter(out_img)
    painter.setBrush(QBrush(image))
    painter.setPen(Qt.NoPen)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.drawEllipse(0, 0, imgsize, imgsize)
    painter.end()

    return QPixmap.fromImage(out_img)


def scale_pixmap(pixmap: QPixmap, size_px: int) -> QPixmap:
    return pixmap.scaled(
        size_px,
        size_px,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )
