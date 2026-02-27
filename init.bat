python -m venv .venv
.venv/Scripts/activate.bat
IF DEFINED VIRTUAL_ENV (
    pip install -r requirements.txt
) ELSE (
    ECHO VIRTUAL_ENV is not set
)

