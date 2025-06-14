"""
Главное окно Optimax Pro с современным темным дизайном
"""

import sys
import os
import logging
import subprocess
import time
import psutil
import wmi
import threading
import socket
import glob
import hashlib
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFrame, QStackedWidget,
    QSlider, QGraphicsDropShadowEffect, QScrollArea, QGridLayout,
    QCheckBox, QMessageBox, QComboBox, QLineEdit, QFileDialog, QTextEdit,
    QTabWidget, QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QPainter, QPen, QIcon, QFont

# Локальные импорты
from ui.widgets import CustomSlider, CircularProgress, ModernButton, TweakCard
from ui.threads import StressTestThread, AIAnalysisThread, OptimizationThread
from tweaks import registry_tweaks, security_tweaks, cleanup_tweaks, performance_tweaks, network_tweaks, optimization_tweaks

# Настройка логирования
logging.basicConfig(
    filename='optimax_log.txt', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OptimaxPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPTIMAX PRO")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)

        # Переменные состояния
        self.is_dark_theme = True
        self.current_profile = "Стандартный"
        self.monitor_data = {"cpu": [], "ram": [], "disk": [], "time": []}
        self.monitor_time = 60

        # Инициализация UI
        self.init_ui()
        self.apply_dark_theme()

        # Таймер мониторинга
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitoring)
        self.monitor_timer.start(1000)

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основная разметка
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Создаем сайдбар
        self.create_sidebar()

        # Создаем область контента
        self.create_content_area()

        # Добавляем виджеты в основную разметку
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_stack)

    def create_sidebar(self):
        """Создание боковой панели навигации"""
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)

        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(8)

        # Заголовок
        title_layout = QHBoxLayout()
        optimax_label = QLabel("OPTIMAX")
        optimax_label.setObjectName("title_optimax")
        pro_label = QLabel("OPTIMAX PRO")
        pro_label.setObjectName("title_pro")

        title_layout.addWidget(optimax_label)
        title_layout.addWidget(pro_label)
        title_layout.addStretch()

        layout.addLayout(title_layout)
        layout.addSpacing(20)

        # Кнопки навигации
        self.nav_buttons = []
        nav_items = [
            ("📊", "Monitoring", "Мониторинг ресурсов системы"),
            ("⚙️", "Optimization", "Оптимизация производительности"),
            ("🧹", "Cleanup", "Очистка системы"),
            ("⚡", "Autostart", "Управление автозагрузкой"),
            ("🤖", "AI Analysis", "AI анализ системы"),
            ("👤", "Profiles", "Профили оптимизации"),
            ("⏰", "Scheduler", "Планировщик задач"),
            ("❓", "Help", "Справка и документация"),
            ("⚙️", "Settings", "Настройки приложения")
        ]

        for icon, text, tooltip in nav_items:
            btn = ModernButton(icon, text, tooltip)
            btn.clicked.connect(lambda checked, idx=len(self.nav_buttons): self.switch_page(idx))
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # Активируем первую кнопку
        if self.nav_buttons:
            self.nav_buttons[0].setActive(True)

    def create_content_area(self):
        """Создание области контента"""
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_stack")

        # Создаем страницы
        self.monitoring_page = self.create_monitoring_page()
        self.optimize_page = self.create_optimize_page()
        self.cleanup_page = self.create_cleanup_page()
        self.autostart_page = self.create_autostart_page()
        self.ai_page = self.create_ai_page()
        self.profiles_page = self.create_profiles_page()
        self.scheduler_page = self.create_scheduler_page()
        self.help_page = self.create_help_page()
        self.settings_page = self.create_settings_page()

        # Добавляем страницы
        self.content_stack.addWidget(self.monitoring_page)
        self.content_stack.addWidget(self.optimize_page)
        self.content_stack.addWidget(self.cleanup_page)
        self.content_stack.addWidget(self.autostart_page)
        self.content_stack.addWidget(self.ai_page)
        self.content_stack.addWidget(self.profiles_page)
        self.content_stack.addWidget(self.scheduler_page)
        self.content_stack.addWidget(self.help_page)
        self.content_stack.addWidget(self.settings_page)

    def create_monitoring_page(self):
        """Создание страницы мониторинга"""
        page = QWidget()
        page.setObjectName("monitoring_page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Заголовок
        title = QLabel("Мониторинг")
        title.setObjectName("page_title")
        layout.addWidget(title)

        # Индикаторы ресурсов
        resources_frame = QFrame()
        resources_frame.setObjectName("resources_frame")
        resources_layout = QHBoxLayout(resources_frame)
        resources_layout.setSpacing(40)

        self.cpu_circle = CircularProgress("CPU", 32)
        self.ram_circle = CircularProgress("RAM", 57) 
        self.disk_circle = CircularProgress("Disk", 21)

        resources_layout.addWidget(self.cpu_circle)
        resources_layout.addWidget(self.ram_circle)
        resources_layout.addWidget(self.disk_circle)

        layout.addWidget(resources_frame)

        # Дополнительная информация
        info_frame = QFrame()
        info_frame.setObjectName("info_frame")
        info_layout = QVBoxLayout(info_frame)

        self.temp_label = QLabel("Температура CPU: Н/Д")
        self.load_label = QLabel("Нагрузка по ядрам: Н/Д")
        self.net_speed_label = QLabel("Скорость интернета: Н/Д")

        info_layout.addWidget(self.temp_label)
        info_layout.addWidget(self.load_label)
        info_layout.addWidget(self.net_speed_label)

        layout.addWidget(info_frame)
        layout.addStretch()

        return page

    def create_optimize_page(self):
        """Создание страницы оптимизации"""
        page = QWidget()
        page.setObjectName("optimize_page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Заголовок
        title = QLabel("Оптимизация")
        title.setObjectName("page_title")
        layout.addWidget(title)

        # Прогресс бар
        self.optimize_progress = QProgressBar()
        self.optimize_progress.setObjectName("progress_bar")
        self.optimize_progress.setTextVisible(True)
        layout.addWidget(self.optimize_progress)

        # Кнопка оптимизации
        optimize_btn = ModernButton("⚡", "Применить выбранные твики", "Запустить оптимизацию")
        optimize_btn.clicked.connect(self.start_optimization)
        layout.addWidget(optimize_btn)

        # Область прокрутки для твиков
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("tweaks_scroll")

        scroll_content = QWidget()
        self.tweaks_layout = QVBoxLayout(scroll_content)

        # Создаем карточки твиков
        self.create_tweak_cards()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        return page

    def create_tweak_cards(self):
        """Создание карточек твиков"""
        categories = {
            "Registry": ("📝", registry_tweaks[:10]),
            "Security": ("🔐", security_tweaks[:10]),
            "Performance": ("⚡", performance_tweaks[:10]),
            "Network": ("🌐", network_tweaks[:10])
        }

        self.tweak_cards = []

        for category_name, (icon, tweaks) in categories.items():
            # Заголовок категории
            category_header = QLabel(f"{icon} {category_name}")
            category_header.setObjectName("category_header")
            self.tweaks_layout.addWidget(category_header)

            # Карточки твиков
            for tweak in tweaks:
                card = TweakCard(tweak)
                self.tweak_cards.append(card)
                self.tweaks_layout.addWidget(card)

            self.tweaks_layout.addSpacing(20)

    def create_cleanup_page(self):
        """Создание страницы очистки"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Очистка")
        title.setObjectName("page_title")
        layout.addWidget(title)

        layout.addStretch()
        return page

    def create_autostart_page(self):
        """Создание страницы автозагрузки"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Autostart")
        title.setObjectName("page_title")
        layout.addWidget(title)

        layout.addStretch()
        return page

    def create_ai_page(self):
        """Создание страницы AI анализа"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("AI Analysis")
        title.setObjectName("page_title")
        layout.addWidget(title)

        layout.addStretch()
        return page

    def create_profiles_page(self):
        """Создание страницы профилей"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Profiles")
        title.setObjectName("page_title")
        layout.addWidget(title)

        layout.addStretch()
        return page

    def create_scheduler_page(self):
        """Создание страницы планировщика"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Scheduler")
        title.setObjectName("page_title")
        layout.addWidget(title)

        layout.addStretch()
        return page

    def create_help_page(self):
        """Создание страницы справки"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Help")
        title.setObjectName("page_title")
        layout.addWidget(title)

        layout.addStretch()
        return page

    def create_settings_page(self):
        """Создание страницы настроек"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Settings")
        title.setObjectName("page_title")
        layout.addWidget(title)

        layout.addStretch()
        return page

    def switch_page(self, index):
        """Переключение страниц"""
        # Деактивируем все кнопки
        for btn in self.nav_buttons:
            btn.setActive(False)

        # Активируем текущую кнопку
        if 0 <= index < len(self.nav_buttons):
            self.nav_buttons[index].setActive(True)

        # Переключаем страницу
        self.content_stack.setCurrentIndex(index)

    def update_monitoring(self):
        """Обновление данных мониторинга"""
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("C:").percent

            self.cpu_circle.setValue(cpu)
            self.ram_circle.setValue(ram)
            self.disk_circle.setValue(disk)

        except Exception as e:
            logging.error(f"Ошибка мониторинга: {e}")

    def start_optimization(self):
        """Запуск оптимизации"""
        selected_tweaks = [card for card in self.tweak_cards if card.is_enabled()]

        if not selected_tweaks:
            QMessageBox.information(self, "Информация", "Выберите твики для применения")
            return

        self.optimization_thread = OptimizationThread(selected_tweaks)
        self.optimization_thread.progress.connect(self.optimize_progress.setValue)
        self.optimization_thread.finished.connect(self.optimization_finished)
        self.optimization_thread.start()

    def optimization_finished(self):
        """Завершение оптимизации"""
        QMessageBox.information(self, "Успех", "Оптимизация завершена!")
        self.optimize_progress.setValue(0)

    def apply_dark_theme(self):
        """Применение темной темы"""
        style = """
        /* Основные стили */
        QMainWindow {
            background-color: #1E1E1E;
            color: #E0E0E0;
        }

        /* Сайдбар */
        QFrame#sidebar {
            background-color: #252525;
            border-right: 1px solid #404040;
        }

        /* Заголовки */
        QLabel#title_optimax {
            color: #E0E0E0;
            font-size: 16px;
            font-weight: bold;
        }

        QLabel#title_pro {
            color: #4A90E2;
            font-size: 16px;
            font-weight: bold;
        }

        QLabel#page_title {
            color: #E0E0E0;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        QLabel#category_header {
            color: #4A90E2;
            font-size: 18px;
            font-weight: bold;
            margin: 20px 0 10px 0;
        }

        /* Область контента */
        QStackedWidget#content_stack {
            background-color: #1E1E1E;
        }

        /* Фреймы */
        QFrame#resources_frame {
            background-color: #2D2D2D;
            border-radius: 15px;
            padding: 30px;
            border: 1px solid #404040;
        }

        QFrame#info_frame {
            background-color: #2D2D2D;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #404040;
        }

        /* Прогресс бар */
        QProgressBar#progress_bar {
            background-color: #404040;
            border-radius: 8px;
            text-align: center;
            color: #E0E0E0;
            font-weight: bold;
            height: 30px;
        }

        QProgressBar#progress_bar::chunk {
            background-color: #4A90E2;
            border-radius: 8px;
        }

        /* Скролл */
        QScrollArea#tweaks_scroll {
            background-color: transparent;
            border: none;
        }

        QScrollBar:vertical {
            background: #404040;
            width: 12px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background: #606060;
            min-height: 20px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical:hover {
            background: #707070;
        }
        """

        self.setStyleSheet(style)
