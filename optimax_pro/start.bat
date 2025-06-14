@echo off
title Optimax Pro
echo Запуск Optimax Pro...
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден! Пожалуйста, установите Python 3.9 или выше.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Проверяем зависимости
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    echo Устанавливаем зависимости...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Ошибка установки зависимостей!
        pause
        exit /b 1
    )
)

REM Запускаем приложение
echo Запуск приложения...
python main.py

pause
