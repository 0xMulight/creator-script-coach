@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set "PYCMD=py -3") else (set "PYCMD=python")
:menu
cls
echo Creator Script Coach - 脚本教练
echo 1. 检查 60 秒短视频脚本
echo 2. 对比修改前后的脚本
echo 3. 运行测试
echo 0. 退出
set /p op=选择：
if "%op%"=="1" %PYCMD% -m creator_script_coach coach --file examples/script.txt --duration 60 --output reports
if "%op%"=="2" %PYCMD% -m creator_script_coach compare --before examples/script.txt --after examples/script-edited.txt --duration 60
if "%op%"=="3" %PYCMD% -m unittest discover -s tests -v
if "%op%"=="0" exit /b 0
echo.
pause
goto menu
