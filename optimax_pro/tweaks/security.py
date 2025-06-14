"""
Твики безопасности для Optimax Pro
"""

import winreg
import subprocess
import logging

def tweak_391_disable_network_discovery():
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

def tweak_392_enable_firewall():
    """Включение брандмауэра
    Повышает безопасность.
    Может блокировать программы."""
    try:
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], check=False)
    except Exception:
        pass

def tweak_393_disable_remote_assistance():
    """Отключение удаленной помощи
    Повышает безопасность.
    Удаленная помощь недоступна."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Policies\Microsoft\Windows\WinRM\WinRMService"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "AllowRemoteAssistance", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

def tweak_394_disable_file_sharing():
    """Отключение общего доступа к файлам
    Повышает безопасность.
    Обмен файлами недоступен."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "AllowFileSharing", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

def tweak_395_enable_secure_boot():
    """Включение безопасной загрузки
    Повышает безопасность.
    Требует поддержки оборудования."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Policies\Microsoft\Windows\DeviceGuard"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "EnableSecureBoot", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_396_disable_guest_account():
    """Отключение гостевой учетной записи
    Повышает безопасность.
    Гостевой доступ недоступен."""
    try:
        subprocess.run(["net", "user", "Guest", "/active:no"], check=False)
    except Exception:
        pass

def tweak_397_enable_password_policy():
    """Включение политики паролей
    Повышает безопасность.
    Требует сложные пароли."""
    try:
        subprocess.run(["net", "accounts", "/minpwlen:8", "/maxpwage:90", "/minpwage:1"], check=False)
    except Exception:
        pass

def tweak_398_disable_autoplay():
    """Отключение автозапуска
    Повышает безопасность.
    Устройства не запускаются автоматически."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "NoDriveTypeAutoRun", 0, winreg.REG_DWORD, 255)
    except Exception:
        pass

def tweak_399_enable_uac():
    """Включение UAC
    Повышает безопасность.
    Может усложнить запуск программ."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "EnableLUA", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass

def tweak_400_disable_admin_sharing():
    """Отключение административного общего доступа
    Повышает безопасность.
    Общий доступ недоступен."""
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "LocalAccountTokenFilterPolicy", 0, winreg.REG_DWORD, 0)
    except Exception:
        pass

security_tweaks = [
    tweak_391_disable_network_discovery, tweak_392_enable_firewall, tweak_393_disable_remote_assistance,
    tweak_394_disable_file_sharing, tweak_395_enable_secure_boot, tweak_396_disable_guest_account,
    tweak_397_enable_password_policy, tweak_398_disable_autoplay, tweak_399_enable_uac,
    tweak_400_disable_admin_sharing
]
