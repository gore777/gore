"""
Твики производительности для Optimax Pro
"""

import winreg
import subprocess

def tweak_471_enable_high_performance():
    """Включение режима высокой производительности
    Увеличивает скорость.
    Увеличивает энергопотребление."""
    try:
        subprocess.run(["powercfg", "-setactive", "SCHEME_MIN"], check=False)
    except Exception:
        pass

def tweak_472_disable_background_services():
    """Отключение фоновых служб
    Снижает нагрузку.
    Может повлиять на функциональность."""
    try:
        services = ["SysMain", "WSearch", "DiagTrack"]
        for service in services:
            subprocess.run(["sc", "config", service, "start=", "disabled"], check=False)
            subprocess.run(["sc", "stop", service], check=False)
    except Exception:
        pass

def tweak_473_enable_cpu_optimization():
    """Оптимизация CPU
    Увеличивает производительность.
    Увеличивает энергопотребление."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Control\Power"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "CsEnabled", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

def tweak_474_disable_disk_defrag():
    """Отключение дефрагментации диска
    Снижает нагрузку.
    Может замедлить диск."""
    try:
        subprocess.run(["schtasks", "/Change", "/TN", "Microsoft\Windows\Defrag\ScheduledDefrag", "/Disable"], check=False)
    except Exception:
        pass

def tweak_475_enable_gpu_optimization():
    """Оптимизация GPU
    Увеличивает производительность.
    Увеличивает энергопотребление."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "SystemResponsiveness", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

def tweak_476_disable_power_saving():
    """Отключение энергосбережения
    Увеличивает производительность.
    Увеличивает энергопотребление."""
    try:
        subprocess.run(["powercfg", "-change", "-standby-timeout-ac", "0"], check=False)
        subprocess.run(["powercfg", "-change", "-hibernate-timeout-ac", "0"], check=False)
    except Exception:
        pass

def tweak_477_enable_memory_optimization():
    """Оптимизация памяти
    Увеличивает производительность.
    Требует больше RAM."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "DisablePagingExecutive", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_478_disable_superfetch():
    """Отключение Superfetch
    Снижает нагрузку.
    Замедляет запуск программ."""
    try:
        subprocess.run(["sc", "config", "SysMain", "start=", "disabled"], check=False)
        subprocess.run(["sc", "stop", "SysMain"], check=False)
    except Exception:
        pass

def tweak_479_enable_fast_boot():
    """Включение быстрой загрузки
    Ускоряет загрузку.
    Может повлиять на стабильность."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager\Power"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "HiberbootEnabled", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_480_disable_indexing_service():
    """Отключение службы индексации
    Снижает нагрузку.
    Замедляет поиск."""
    try:
        subprocess.run(["sc", "config", "WSearch", "start=", "disabled"], check=False)
        subprocess.run(["sc", "stop", "WSearch"], check=False)
    except Exception:
        pass

performance_tweaks = [
    tweak_471_enable_high_performance, tweak_472_disable_background_services, tweak_473_enable_cpu_optimization,
    tweak_474_disable_disk_defrag, tweak_475_enable_gpu_optimization, tweak_476_disable_power_saving,
    tweak_477_enable_memory_optimization, tweak_478_disable_superfetch, tweak_479_enable_fast_boot,
    tweak_480_disable_indexing_service
]
