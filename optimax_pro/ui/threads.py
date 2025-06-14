"""
Рабочие потоки для Optimax Pro
"""

import time
import psutil
import wmi
import logging
from PyQt6.QtCore import QThread, pyqtSignal

class StressTestThread(QThread):
    """Поток стресс-тестирования CPU"""
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        """Запуск стресс-теста"""
        try:
            for i in range(100):
                # Создаем нагрузку на CPU
                for _ in range(1000000):
                    _ = 2 ** 20

                self.progress.emit(i + 1)
                time.sleep(0.1)

        except Exception as e:
            logging.error(f"Ошибка стресс-теста: {e}")
        finally:
            self.finished.emit()

class AIAnalysisThread(QThread):
    """Поток AI анализа системы"""
    result = pyqtSignal(str)

    def run(self):
        """Запуск анализа"""
        try:
            # Получаем данные о системе
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage("C:").percent
            temp = self.get_cpu_temp()

            # Вычисляем оценку
            score = 100 - (cpu_usage * 0.3 + ram_usage * 0.4 + disk_usage * 0.2 + (temp / 100) * 0.1)

            # Формируем рекомендации
            recommendations = []

            if cpu_usage > 80:
                recommendations.append("🔥 Высокая нагрузка CPU. Рекомендуется закрыть лишние процессы.")
            if ram_usage > 90:
                recommendations.append("🔥 Недостаток RAM. Увеличьте объём памяти или закройте приложения.")
            if disk_usage > 95:
                recommendations.append("💾 Диск переполнен. Очистите ненужные файлы.")
            if temp > 85:
                recommendations.append("🌡️ Перегрев CPU. Проверьте охлаждение.")

            if not recommendations:
                recommendations.append("✅ Система работает нормально!")

            # Формируем результат
            result_text = f"Оценка системы: {score:.1f}/100\n\n"
            result_text += "Рекомендации:\n"
            result_text += "\n".join(recommendations)

            self.result.emit(result_text)

        except Exception as e:
            logging.error(f"Ошибка AI анализа: {e}")
            self.result.emit("Ошибка при анализе системы")

    def get_cpu_temp(self):
        """Получение температуры CPU"""
        try:
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            sensors = w.Sensor()
            for sensor in sensors:
                if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
                    return sensor.Value
            return 50  # Значение по умолчанию
        except Exception:
            return 50  # Значение по умолчанию

class OptimizationThread(QThread):
    """Поток оптимизации системы"""
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, tweak_cards):
        super().__init__()
        self.tweak_cards = tweak_cards

    def run(self):
        """Запуск оптимизации"""
        try:
            total_tweaks = len(self.tweak_cards)

            for i, card in enumerate(self.tweak_cards):
                try:
                    # Выполняем твик
                    card.tweak_function()

                    # Обновляем прогресс
                    progress = int((i + 1) / total_tweaks * 100)
                    self.progress.emit(progress)

                    # Небольшая задержка для визуального эффекта
                    time.sleep(0.1)

                except Exception as e:
                    logging.error(f"Ошибка выполнения твика {card.title}: {e}")

        except Exception as e:
            logging.error(f"Ошибка оптимизации: {e}")
        finally:
            self.finished.emit()

class CleanupThread(QThread):
    """Поток очистки системы"""
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, cleanup_functions):
        super().__init__()
        self.cleanup_functions = cleanup_functions

    def run(self):
        """Запуск очистки"""
        try:
            total_tasks = len(self.cleanup_functions)

            for i, cleanup_func in enumerate(self.cleanup_functions):
                try:
                    cleanup_func()

                    progress = int((i + 1) / total_tasks * 100)
                    self.progress.emit(progress)

                    time.sleep(0.1)

                except Exception as e:
                    logging.error(f"Ошибка очистки: {e}")

        except Exception as e:
            logging.error(f"Ошибка процесса очистки: {e}")
        finally:
            self.finished.emit()
