@echo off
cd /d %~dp0
set PYTHONPATH=.

echo Running box_with_door.py...
python parametric_cad\examples\box_with_door.py

echo Running hollow_box.py...
python parametric_cad\examples\hollow_box.py

echo Running spur_gear_example.py...
python parametric_cad\examples\spur_gear_example.py

echo.
echo Checking box_with_door_output folder...
if exist output\box_with_door_output (
    dir output\box_with_door_output
) else (
    echo ERROR: box_with_door_output folder does not exist!
)

echo.
echo Checking hollow_box_output folder...
if exist output\hollow_box_output (
    dir output\hollow_box_output
) else (
    echo ERROR: hollow_box_output folder does not exist!
)

echo.
echo Checking spur_gear_example_output folder...
if exist output\spur_gear_example_output (
    dir output\spur_gear_example_output
) else (
    echo ERROR: spur_gear_example_output folder does not exist!
)

pause
