@echo off
title Установка зависимостей Optimax Pro
echo Установка зависимостей для Optimax Pro...
echo.

REM Обновляем pip
echo Обновляем pip...
python -m pip install --upgrade pip

REM Устанавливаем зависимости
echo Устанавливаем зависимости...
pip install -r requirements.txt

if errorlevel 1 (
    echo Ошибка установки зависимостей!
    pause
    exit /b 1
) else (
    echo Зависимости успешно установлены!
    echo Теперь вы можете запустить start.bat
    pause
)
