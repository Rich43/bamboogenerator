@echo off
REM Run all Python examples using the cross-platform script
cd /d %~dp0
set PYTHONPATH=.

python run_examples.py

pause
