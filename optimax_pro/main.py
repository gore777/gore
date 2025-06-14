import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFrame, QStackedWidget,
    QScrollArea, QGridLayout, QSizePolicy, QTableWidget
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QIcon

# --- Кастомные компоненты ---

class CircularProgress(QWidget):
    def __init__(self, label, max_value=100):
        super().__init__()
        self.value = 0
        self.max_value = max_value
        self.label = label
        self.setFixedSize(150, 150)

    def setValue(self, val):
        self.value = min(max(val, 0), self.max_value)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(10, 10, -10, -10)
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 2
        # Фон
        painter.setBrush(QColor(50, 50, 50))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius, radius)
        # Угол прогресса
        angle_span = int(360 * self.value / self.max_value)
        pen = QPen(QColor(70, 130, 180), 12)
        painter.setPen(pen)
        painter.drawArc(rect, 90 * 16, -angle_span * 16)
        # Текст
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self.label}\n{self.value:.0f}%")

class ToggleSwitch(QPushButton):
    def __init__(self, label_on="ON", label_off="OFF"):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(False)
        self.setFixedSize(60, 30)
        self.update_style()

        self.toggled.connect(self.update_style)

    def update_style(self):
        if self.isChecked():
            self.setText("ON")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    border-radius: 15px;
                    color: white;
                    font-weight: bold;
                }
            """)
        else:
            self.setText("OFF")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #C0C0C0;
                    border-radius: 15px;
                    color: black;
                    font-weight: bold;
                }
            """)

class TweakCard(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setFixedSize(250, 120)
        self.setStyleSheet("""
            QWidget {
                background-color: #2A2A2A;
                border-radius: 12px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        self.label = QLabel(title)
        self.label.setStyleSheet("color: #E0E0E0; font-size: 14px;")
        self.toggle = ToggleSwitch()
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.toggle)

    def is_enabled(self):
        return self.toggle.isChecked()

# --- Основное окно ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OptimaxPro")
        self.setGeometry(100, 100, 1300, 800)
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(self.style_sheet())

        self.init_ui()

    def style_sheet(self):
        return """
        QMainWindow {
            background-color: #1E1E1E;
        }
        QLabel#title {
            color: #FFFFFF;
            font-size: 20px;
            font-weight: bold;
        }
        QPushButton {
            border: none;
            background-color: transparent;
            color: #FFFFFF;
            font-size: 16px;
        }
        QPushButton#menuBtn {
            font-size: 24px;
        }
        QFrame#sidebar {
            background-color: #252525;
        }
        QLabel#sectionTitle {
            color: #FFFFFF;
            font-size: 18px;
            font-weight: bold;
        }
        QProgressBar {
            background-color: #404040;
            border-radius: 8px;
            height: 20px;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 8px;
        }
        QScrollArea {
            border: none;
        }
        """

    def init_ui(self):
        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Сайдбар
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(20)

        # Заголовок
        title_label = QLabel("OptimaxPro")
        title_label.setObjectName("title")
        sidebar_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопки навигации
        self.btn_monitoring = QPushButton("📊 Мониторинг")
        self.btn_optimization = QPushButton("⚙️ Оптимизация")
        self.btn_cleanup = QPushButton("🧹 Очистка")
        self.btn_ai = QPushButton("🤖 AI Анализ")
        self.btn_profiles = QPushButton("👤 Профили")
        self.btn_scheduler = QPushButton("⏰ Планировщик")
        self.btn_help = QPushButton("❓ Справка")
        self.btn_settings = QPushButton("⚙️ Настройки")

        for btn in [self.btn_monitoring, self.btn_optimization, self.btn_cleanup,
                    self.btn_ai, self.btn_profiles, self.btn_scheduler,
                    self.btn_help, self.btn_settings]:
            btn.setStyleSheet("""
                QPushButton {
                    color: #FFFFFF;
                    font-size: 16px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #3A3A3A;
                    border-radius: 8px;
                }
            """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Контент
        self.stack = QStackedWidget()

        # Страницы
        self.page_monitoring = self.create_monitoring_page()
        self.page_optimization = self.create_optimization_page()
        self.page_cleanup = self.create_cleanup_page()
        self.page_ai = self.create_ai_page()
        self.page_profiles = self.create_profiles_page()
        self.page_scheduler = self.create_scheduler_page()
        self.page_help = self.create_help_page()
        self.page_settings = self.create_settings_page()

        self.stack.addWidget(self.page_monitoring)
        self.stack.addWidget(self.page_optimization)
        self.stack.addWidget(self.page_cleanup)
        self.stack.addWidget(self.page_ai)
        self.stack.addWidget(self.page_profiles)
        self.stack.addWidget(self.page_scheduler)
        self.stack.addWidget(self.page_help)
        self.stack.addWidget(self.page_settings)

        # Связь кнопок
        self.btn_monitoring.clicked.connect(lambda: self.switch_page(0))
        self.btn_optimization.clicked.connect(lambda: self.switch_page(1))
        self.btn_cleanup.clicked.connect(lambda: self.switch_page(2))
        self.btn_ai.clicked.connect(lambda: self.switch_page(3))
        self.btn_profiles.clicked.connect(lambda: self.switch_page(4))
        self.btn_scheduler.clicked.connect(lambda: self.switch_page(5))
        self.btn_help.clicked.connect(lambda: self.switch_page(6))
        self.btn_settings.clicked.connect(lambda: self.switch_page(7))

        # Расположение
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        # Изначально
        self.switch_page(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def create_monitoring_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        title = QLabel("Мониторинг")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Индикаторы
        indicators_layout = QHBoxLayout()
        self.cpu_indicator = CircularProgress("CPU", 100)
        self.ram_indicator = CircularProgress("RAM", 100)
        self.disk_indicator = CircularProgress("Disk", 100)
        indicators_layout.addWidget(self.cpu_indicator)
        indicators_layout.addWidget(self.ram_indicator)
        indicators_layout.addWidget(self.disk_indicator)
        layout.addLayout(indicators_layout)

        # Обновление данных
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitoring)
        self.monitor_timer.start(1000)

        return page

    def update_monitoring(self):
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("C:").percent
        self.cpu_indicator.setValue(cpu)
        self.ram_indicator.setValue(ram)
        self.disk_indicator.setValue(disk)

    def create_optimization_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Оптимизация")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Карточки твиков
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        grid = QGridLayout(content)
        grid.setSpacing(15)

        # Пример карточек
        tweaks = ["Registry Tweaks", "Security Tweaks", "Performance Tweaks", "Network Tweaks"]
        self.tweak_cards = []

        for i, name in enumerate(tweaks):
            card = TweakCard(name)
            row = i // 2
            col = i % 2
            grid.addWidget(card, row, col)
            self.tweak_cards.append(card)

        scroll.setWidget(content)
        layout.addWidget(scroll)

        # Кнопка применить
        btn_apply = QPushButton("Применить")
        btn_apply.setFixedSize(150, 40)
        btn_apply.clicked.connect(self.apply_tweaks)
        layout.addWidget(btn_apply, alignment=Qt.AlignmentFlag.AlignRight)

        return page

    def apply_tweaks(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        # Тут логика применения твиков
        # Для примера просто имитируем прогресс
        for i in range(1, 101, 10):
            self.progress_bar.setValue(i)
            QApplication.processEvents()
        self.progress_bar.hide()

    def create_cleanup_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Очистка системы")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        btn_temp = QPushButton("Очистить временные файлы")
        btn_temp.setFixedSize(200, 40)
        layout.addWidget(btn_temp)

        btn_cache = QPushButton("Очистить кэш браузеров")
        btn_cache.setFixedSize(200, 40)
        layout.addWidget(btn_cache)

        btn_registry = QPushButton("Очистить реестр")
        btn_registry.setFixedSize(200, 40)
        layout.addWidget(btn_registry)

        return page

    def create_ai_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("AI Анализ")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        btn_start = QPushButton("Запустить анализ")
        btn_start.setFixedSize(200, 40)
        layout.addWidget(btn_start)

        self.ai_result = QLabel("Результаты анализа появятся здесь")
        self.ai_result.setWordWrap(True)
        layout.addWidget(self.ai_result)

        return page

    def create_profiles_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Профили")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Пример профилей
        profiles = ["Стандартный", "Игровой", "Энергосберегающий"]
        for p in profiles:
            btn = QPushButton(p)
            btn.setFixedSize(200, 40)
            layout.addWidget(btn)

        return page

    def create_scheduler_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Планировщик задач")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Таблица задач
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Задача", "Время", "Параметры"])
        layout.addWidget(table)

        btn_add = QPushButton("Добавить задачу")
        btn_add.setFixedSize(180, 40)
        layout.addWidget(btn_add, alignment=Qt.AlignmentFlag.AlignRight)

        return page

    def create_help_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        label = QLabel("Справка и инструкции")
        label.setObjectName("sectionTitle")
        layout.addWidget(label)

        text = QLabel("Здесь будет подробная документация и инструкции по использованию.")
        text.setWordWrap(True)
        layout.addWidget(text)

        return page

    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Настройки")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Тема
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Тема:")
        theme_label.setStyleSheet("color: #FFFFFF; font-size: 16px;")
        theme_slider = QScrollArea()
        theme_slider.setFixedSize(100, 40)
        theme_slider_widget = QWidget()
        theme_slider_layout = QHBoxLayout(theme_slider_widget)
        theme_slider_layout.setContentsMargins(0, 0, 0, 0)
        theme_slider_layout.setSpacing(10)
        btn_dark = QPushButton("Темная")
        btn_light = QPushButton("Светлая")
        theme_slider_layout.addWidget(btn_dark)
        theme_slider_layout.addWidget(btn_light)
        theme_slider.setWidget(theme_slider_widget)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(btn_dark)
        theme_layout.addWidget(btn_light)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        # Точка восстановления
        btn_restore = QPushButton("Создать точку восстановления")
        btn_restore.setFixedSize(250, 40)
        layout.addWidget(btn_restore)

        return page

# --- Запуск ---

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
