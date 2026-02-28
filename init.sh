python -m venv .venv
source .venv/bin/activate
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "Virtual environment is NOT activated."
else
  pip install -r requirements.txt
fi

echo "run 'source .venv/bin/active' to enable virtual environment"
