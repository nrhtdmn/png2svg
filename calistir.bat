@echo off
title Askeri Isaretler PNG-SVG Donusturucu
echo.
echo  Askeri Isaretler PNG-SVG Donusturucu baslatiliyor...
echo.

REM Python kontrolu
where python >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON=python
    goto CALISTIR
)

REM Python314 kontrolu
if exist "C:\python314\python.exe" (
    set PYTHON=C:\python314\python.exe
    goto CALISTIR
)

REM Python311 kontrolu
if exist "C:\python311\python.exe" (
    set PYTHON=C:\python311\python.exe
    goto CALISTIR
)

echo  HATA: Python bulunamadi!
echo  Lutfen Python kurun: https://python.org
pause
exit

:CALISTIR
echo  Python: %PYTHON%
echo.

REM Pillow kurulu mu kontrol et
%PYTHON% -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo  Pillow kuruluyor...
    %PYTHON% -m pip install Pillow
    echo.
)

REM Programi calistir
%PYTHON% "%~dp0inkscape_donusturucu.py"

if %errorlevel% neq 0 (
    echo.
    echo  HATA olustu! Hata kodunu not alin.
    pause
)
