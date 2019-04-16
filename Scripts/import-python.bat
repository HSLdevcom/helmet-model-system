@REM This script imports all required Python dependencies to system PATH for this session
@REM set EMME_PYTHON_PATH=%ProgramFiles%/INRO/Emme/Emme 4/Emme-4.3.3/Python27/
@REM set PATH=%PATH%;%APPDATA%/Python/Scripts/;%EMME_PYTHON_PATH%
set MY_PYTHON_PATH=C:/Python27/
set PATH=%MY_PYTHON_PATH%;%MY_PYTHON_PATH%/Scripts/;%APPDATA%/Python/Scripts/;%PATH%
@REM import dependencies.
set PYTHONPATH=%PYTHONPATH%;./pythonlibs/
