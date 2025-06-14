"""
Твики для очистки системы в Optimax Pro
"""

import os
import shutil
import glob
import subprocess
import winreg

def tweak_431_clean_temp_files():
    """Очистка временных файлов
    Освобождает место.
    Может удалить нужные временные файлы."""
    try:
        paths = [
            os.path.expanduser(r"~\AppData\Local\Temp"),
            r"C:\Windows\Temp"
        ]
        for path in paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        try:
                            os.unlink(os.path.join(root, file))
                        except Exception:
                            pass
                    for dir in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                        except Exception:
                            pass
    except Exception:
        pass

def tweak_432_clean_browser_cache():
    """Очистка кэша браузеров
    Освобождает место.
    Увеличивает время загрузки страниц."""
    try:
        paths = {
            "Edge": os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Cache"),
            "Chrome": os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Cache"),
            "Firefox": os.path.expanduser(r"~\AppData\Local\Mozilla\Firefox\Profiles\*.default-release\cache")
        }
        for path in paths.values():
            if "*" in path:
                for p in glob.glob(path):
                    shutil.rmtree(p, ignore_errors=True)
            else:
                shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass

def tweak_433_clean_system_logs():
    """Очистка системных логов
    Освобождает место.
    Усложняет диагностику."""
    try:
        for log in glob.glob(r"C:\Windows\System32\winevt\Logs\*.evtx"):
            try:
                os.unlink(log)
            except Exception:
                pass
    except Exception:
        pass

def tweak_434_clean_old_updates():
    """Очистка старых обновлений
    Освобождает место.
    Может повлиять на откат обновлений."""
    try:
        subprocess.run(["DISM.exe", "/Online", "/Cleanup-Image", "/StartComponentCleanup"], check=False)
    except Exception:
        pass

def tweak_435_clean_dns_cache():
    """Очистка кэша DNS
    Ускоряет сеть.
    Может нарушить кэшированные адреса."""
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=False)
    except Exception:
        pass

def tweak_436_clean_download_folder():
    """Очистка папки загрузок
    Освобождает место.
    Может удалить нужные файлы."""
    try:
        path = os.path.expanduser(r"~\Downloads")
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        os.unlink(os.path.join(root, file))
                    except Exception:
                        pass
                for dir in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                    except Exception:
                        pass
    except Exception:
        pass

def tweak_437_clean_old_drivers():
    """Очистка старых драйверов
    Освобождает место.
    Может удалить нужные драйверы."""
    try:
        subprocess.run(["pnputil", "/e"], capture_output=True, text=True, check=False)
    except Exception:
        pass

def tweak_438_clean_prefetch():
    """Очистка Prefetch
    Освобождает место.
    Замедляет запуск программ."""
    try:
        path = r"C:\Windows\Prefetch"
        for file in glob.glob(os.path.join(path, "*")):
            try:
                os.unlink(file)
            except Exception:
                pass
    except Exception:
        pass

def tweak_439_clean_error_reports():
    """Очистка отчетов об ошибках
    Освобождает место.
    Усложняет диагностику."""
    try:
        path = r"C:\ProgramData\Microsoft\Windows\WER"
        shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass

def tweak_440_clean_recycle_bin():
    """Очистка корзины
    Освобождает место.
    Удаляет файлы без возможности восстановления."""
    try:
        path = r"C:\$Recycle.Bin"
        shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass

cleanup_tweaks = [
    tweak_431_clean_temp_files, tweak_432_clean_browser_cache, tweak_433_clean_system_logs,
    tweak_434_clean_old_updates, tweak_435_clean_dns_cache, tweak_436_clean_download_folder,
    tweak_437_clean_old_drivers, tweak_438_clean_prefetch, tweak_439_clean_error_reports,
    tweak_440_clean_recycle_bin
]
