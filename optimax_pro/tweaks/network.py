"""
Сетевые твики для Optimax Pro
"""

import subprocess
import winreg

def tweak_511_enable_tcp_optimization():
    """Оптимизация TCP
    Ускоряет сеть.
    Может повлиять на стабильность."""
    try:
        subprocess.run(["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"], check=False)
    except Exception:
        pass

def tweak_512_enable_rss():
    """Включение RSS
    Ускоряет сеть.
    Требует поддержки оборудования."""
    try:
        subprocess.run(["netsh", "int", "tcp", "set", "global", "rss=enabled"], check=False)
    except Exception:
        pass

def tweak_513_disable_nagle():
    """Отключение алгоритма Нейгла
    Ускоряет сеть.
    Может увеличить задержки."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "TcpNoDelay", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_514_enable_fast_dns():
    """Включение быстрого DNS
    Ускоряет сеть.
    Требует настройки."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "FastDNS", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_515_disable_network_throttling():
    """Отключение троттлинга сети
    Ускоряет сеть.
    Увеличивает нагрузку."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "NetworkThrottlingIndex", 0, winreg.REG_DWORD, 0xFFFFFFFF)
    except Exception:
        pass

def tweak_516_enable_bandwidth_optimization():
    """Оптимизация пропускной способности
    Ускоряет сеть.
    Увеличивает нагрузку."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Policies\Microsoft\Psched"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "NonBestEffortLimit", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

def tweak_517_disable_wifi_background():
    """Отключение фонового сканирования Wi-Fi
    Снижает нагрузку.
    Замедляет подключение."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Policies\Microsoft\Windows\WcmSvc"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "DisableBackgroundScan", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_518_enable_low_latency():
    """Включение низкой задержки
    Ускоряет сеть.
    Увеличивает нагрузку."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_519_disable_network_discovery():
    """Отключение обнаружения сети
    Повышает безопасность.
    Устройства в сети не видны."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Policies\Microsoft\Windows\Network Connections"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "NC_StdDomainUserSetLocation", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

def tweak_520_enable_dns_cache():
    """Включение кэша DNS
    Ускоряет сеть.
    Требует ресурсов."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Services\Dnscache\Parameters"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "CacheHashTableBucketSize", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

network_tweaks = [
    tweak_511_enable_tcp_optimization, tweak_512_enable_rss, tweak_513_disable_nagle,
    tweak_514_enable_fast_dns, tweak_515_disable_network_throttling, tweak_516_enable_bandwidth_optimization,
    tweak_517_disable_wifi_background, tweak_518_enable_low_latency, tweak_519_disable_network_discovery,
    tweak_520_enable_dns_cache
]
