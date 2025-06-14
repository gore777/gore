"""
Модуль твиков для Optimax Pro
"""

from .registry import registry_tweaks
from .security import security_tweaks
from .cleanup import cleanup_tweaks
from .performance import performance_tweaks
from .network import network_tweaks

optimization_tweaks = registry_tweaks + security_tweaks + cleanup_tweaks + performance_tweaks + network_tweaks
