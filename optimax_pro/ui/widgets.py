"""
Кастомные виджеты для Optimax Pro
"""

from PyQt6.QtWidgets import QSlider, QWidget, QPushButton, QHBoxLayout, QLabel, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QBrush, QRadialGradient

class CustomSlider(QSlider):
    """Кастомный слайдер с блокировкой колеса мыши"""
    def __init__(self, orientation):
        super().__init__(orientation)

    def wheelEvent(self, event):
        """Блокировка колесика мыши если нет фокуса"""
        if not self.hasFocus():
            event.ignore()
        else:
            super().wheelEvent(event)

class CircularProgress(QWidget):
    """Круговой индикатор прогресса"""
    def __init__(self, label, value=0, max_value=100):
        super().__init__()
        self.value = value
        self.max_value = max_value
        self.label = label
        self.setFixedSize(120, 120)

    def setValue(self, value):
        """Установка значения"""
        self.value = min(value, self.max_value)
        self.update()

    def paintEvent(self, event):
        """Отрисовка индикатора"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2 - 10

        # Фон круга
        painter.setPen(Qt.PenStyle.NoPen)
        bg_color = QColor(60, 60, 60, 100)
        painter.setBrush(bg_color)
        painter.drawEllipse(center, radius, radius)

        # Прогресс
        pen = QPen(QColor(74, 144, 226), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        angle = int(360 * (self.value / self.max_value) * 16)
        painter.drawArc(rect.adjusted(10, 10, -10, -10), 90 * 16, -angle)

        # Текст внутри
        font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        painter.setFont(font)

        # Метка
        painter.setPen(QColor(224, 224, 224))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.label}")

        # Значение
        value_rect = rect.adjusted(0, 20, 0, 0)
        painter.setPen(QColor(74, 144, 226))
        painter.drawText(value_rect, Qt.AlignmentFlag.AlignCenter, f"{self.value}%")

class ModernButton(QPushButton):
    """Современная кнопка с иконкой и текстом"""
    def __init__(self, icon, text, tooltip=""):
        super().__init__()
        self.setObjectName("modern_button")
        self.setCheckable(True)
        self.setToolTip(tooltip)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # Иконка
        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("button_icon")
        layout.addWidget(self.icon_label)

        # Текст
        self.text_label = QLabel(text)
        self.text_label.setObjectName("button_text")
        layout.addWidget(self.text_label)

        layout.addStretch()

        # Стиль
        self.setStyleSheet("""
            QPushButton#modern_button {
                background-color: transparent;
                border: none;
                color: #E0E0E0;
                text-align: left;
                padding: 10px;
                border-radius: 10px;
            }

            QPushButton#modern_button:hover {
                background-color: #3A3A3A;
            }

            QPushButton#modern_button:checked {
                background-color: #4A90E2;
            }

            QLabel#button_icon {
                font-size: 16px;
            }

            QLabel#button_text {
                color: #E0E0E0;
                font-size: 14px;
            }
        """)

    def setActive(self, active):
        """Установка активного состояния"""
        self.setChecked(active)

class TweakCard(QFrame):
    """Карточка твика"""
    def __init__(self, tweak_function):
        super().__init__()
        self.tweak_function = tweak_function
        self.enabled = False

        self.setObjectName("tweak_card")
        self.setFixedHeight(80)

        # Название и описание из докстринга
        doc_lines = tweak_function.__doc__.strip().split('\n')
        self.title = doc_lines[0] if doc_lines else "Неизвестный твик"
        self.description = doc_lines[1] if len(doc_lines) > 1 else "Нет описания"
        self.risks = doc_lines[2] if len(doc_lines) > 2 else "Нет информации о рисках"

        self.init_ui()

    def init_ui(self):
        """Инициализация UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)

        # Левая часть с названием и описанием
        left_layout = QVBoxLayout()

        title_label = QLabel(self.title)
        title_label.setObjectName("tweak_title")

        desc_label = QLabel(self.description)
        desc_label.setObjectName("tweak_desc")

        left_layout.addWidget(title_label)
        left_layout.addWidget(desc_label)

        # Правая часть с переключателем
        self.toggle_btn = QPushButton("OFF")
        self.toggle_btn.setObjectName("tweak_toggle")
        self.toggle_btn.setFixedSize(60, 30)
        self.toggle_btn.clicked.connect(self.toggle)

        layout.addLayout(left_layout)
        layout.addWidget(self.toggle_btn)

        # Стиль
        self.setStyleSheet("""
            QFrame#tweak_card {
                background-color: #2D2D2D;
                border-radius: 10px;
                border: 1px solid #404040;
            }

            QLabel#tweak_title {
                color: #E0E0E0;
                font-size: 14px;
                font-weight: bold;
            }

            QLabel#tweak_desc {
                color: #A0A0A0;
                font-size: 12px;
            }

            QPushButton#tweak_toggle {
                background-color: #404040;
                color: #E0E0E0;
                border-radius: 15px;
                font-weight: bold;
            }

            QPushButton#tweak_toggle[enabled="true"] {
                background-color: #4A90E2;
            }
        """)

    def toggle(self):
        """Переключение состояния"""
        self.enabled = not self.enabled

        if self.enabled:
            self.toggle_btn.setText("ON")
            self.toggle_btn.setProperty("enabled", "true")
        else:
            self.toggle_btn.setText("OFF")
            self.toggle_btn.setProperty("enabled", "false")

        self.toggle_btn.style().unpolish(self.toggle_btn)
        self.toggle_btn.style().polish(self.toggle_btn)

    def is_enabled(self):
        """Проверка включен ли твик"""
        return self.enabled
