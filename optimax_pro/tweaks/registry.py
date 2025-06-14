"""
Твики реестра для Optimax Pro
"""

import winreg
import subprocess
import os
import shutil
import glob
import logging

def tweak_351_disable_registry_logging():
    """Отключение логирования реестра
    Снижает нагрузку на диск.
    Усложняет отладку."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "DisableRegistryLogging", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_352_clear_registry_temp():
    """Очистка временных записей реестра
    Освобождает место.
    Может повлиять на некоторые программы."""
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            for i in range(winreg.QueryInfoKey(reg_key)[0] - 1, -1, -1):
                name = winreg.EnumKey(reg_key, i)
                if "Temp" in name:
                    try:
                        winreg.DeleteKey(reg_key, name)
                    except:
                        pass
    except Exception:
        pass

def tweak_353_disable_uac():
    """Отключение контроля учетных записей (UAC)
    Упрощает запуск программ.
    Уменьшает безопасность."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "EnableLUA", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

def tweak_354_disable_autorun():
    """Отключение автозапуска устройств
    Повышает безопасность.
    Устройства не будут запускаться автоматически."""
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 255)
    except Exception:
        pass

def tweak_355_enable_fast_shutdown():
    """Ускорение выключения системы
    Уменьшает время завершения работы.
    Может привести к потере данных."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Control"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "WaitToKillServiceTimeout", 0, winreg.REG_SZ, "2000")
    except Exception:
        pass

def tweak_356_disable_error_reporting():
    """Отключение отчетов об ошибках
    Снижает нагрузку.
    Усложняет диагностику."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows\Windows Error Reporting"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "Disabled", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_357_disable_thumbnail_cache():
    """Отключение кэша миниатюр
    Освобождает место.
    Увеличивает время загрузки миниатюр."""
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "DisableThumbnailCache", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_358_disable_menu_delay():
    """Уменьшение задержки меню
    Ускоряет открытие меню.
    Может повлиять на анимацию."""
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Control Panel\Desktop"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "MenuShowDelay", 0, winreg.REG_SZ, "100")
    except Exception:
        pass

def tweak_359_disable_system_restore():
    """Отключение восстановления системы
    Освобождает место.
    Убирает возможность восстановления."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Policies\Microsoft\Windows NT\SystemRestore"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "DisableSR", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_360_enable_large_cache():
    """Включение большого системного кэша
    Ускоряет работу с файлами.
    Требует больше RAM."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "LargeSystemCache", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_361_disable_background_apps():
    """Отключение фоновых приложений
    Снижает нагрузку.
    Некоторые приложения перестанут работать в фоне."""
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "GlobalUserDisabled", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_362_disable_taskbar_animations():
    """Отключение анимаций панели задач
    Ускоряет интерфейс.
    Убирает визуальные эффекты."""
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "TaskbarAnimations", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

registry_tweaks = [
    tweak_351_disable_registry_logging, tweak_352_clear_registry_temp, tweak_353_disable_uac,
    tweak_354_disable_autorun, tweak_355_enable_fast_shutdown, tweak_356_disable_error_reporting,
    tweak_357_disable_thumbnail_cache, tweak_358_disable_menu_delay, tweak_359_disable_system_restore,
    tweak_360_enable_large_cache, tweak_361_disable_background_apps, tweak_362_disable_taskbar_animations
]
