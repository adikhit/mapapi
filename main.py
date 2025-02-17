import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QImage, QKeyEvent
from PyQt6.QtCore import Qt
import requests
from io import BytesIO

class MapViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.latitude = 55
        self.longitude = 37
        self.scale = 10

        self.initUI()

    def initUI(self):
        self.setWindowTitle("mapapi")

        latitude_label = QLabel("Широта:")
        self.latitude_edit = QLineEdit(str(self.latitude))

        longitude_label = QLabel("Долгота:")
        self.longitude_edit = QLineEdit(str(self.longitude))

        scale_label = QLabel("Масштаб:")
        self.scale_edit = QLineEdit(str(self.scale))
        self.scale_edit.setEnabled(False)

        update_button = QPushButton("Обновить карту")
        update_button.clicked.connect(self.update_map)

        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hbox_latitude = QHBoxLayout()
        hbox_latitude.addWidget(latitude_label)
        hbox_latitude.addWidget(self.latitude_edit)

        hbox_longitude = QHBoxLayout()
        hbox_longitude.addWidget(longitude_label)
        hbox_longitude.addWidget(self.longitude_edit)

        hbox_scale = QHBoxLayout()
        hbox_scale.addWidget(scale_label)
        hbox_scale.addWidget(self.scale_edit)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_latitude)
        vbox.addLayout(hbox_longitude)
        vbox.addLayout(hbox_scale)
        vbox.addWidget(update_button)
        vbox.addWidget(self.map_label)

        self.setLayout(vbox)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.update_map()
        self.show()

    def keyPressEvent(self, event: QKeyEvent):
        # сдвиги
        if event.key() == Qt.Key.Key_PageUp:
            self.change_scale(1)
        elif event.key() == Qt.Key.Key_PageDown:
            self.change_scale(-1)
        elif event.key() == Qt.Key.Key_Up:
            self.move_map(1, 0)  # Сдвиг вверх
        elif event.key() == Qt.Key.Key_Down:
            self.move_map(-1, 0)  # Сдвиг вниз
        elif event.key() == Qt.Key.Key_Left:
            self.move_map(0, -1)  # Сдвиг влево
        elif event.key() == Qt.Key.Key_Right:
            self.move_map(0, 1)  # Сдвиг вправо

    def change_scale(self, delta):
        self.scale += delta
        self.scale = max(0, min(self.scale, 19))
        self.scale_edit.setText(str(self.scale))
        self.update_map()

    def move_map(self, lat_delta, lon_delta):
        self.latitude += lat_delta
        self.longitude += lon_delta

        # Ограничение координат
        self.latitude = max(-90, min(self.latitude, 90))
        self.longitude = max(-180, min(self.longitude, 180))


        self.latitude_edit.setText(str(self.latitude))
        self.longitude_edit.setText(str(self.longitude))
        self.update_map()

    def update_map(self):
        # обновление карты
        try:
            # Получаем значения из полей ввода, если они есть
            try:
                self.latitude = float(self.latitude_edit.text())
                self.longitude = float(self.longitude_edit.text())
            except ValueError:
                pass

            self.scale_edit.setText(str(self.scale))

            map_url = f"https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&z={self.scale}&l=map"
            response = requests.get(map_url)
            response.raise_for_status()

            image = QImage.fromData(response.content)
            pixmap = QPixmap.fromImage(image)
            self.map_label.setPixmap(pixmap)


        except ValueError as e:
            self.map_label.setText(f"Ошибка: {e}")
        except requests.exceptions.RequestException as e:
            self.map_label.setText(f"Ошибка сети: {e}")
        except Exception as e:
            self.map_label.setText(f"Неизвестная ошибка: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapViewer()
    sys.exit(app.exec())