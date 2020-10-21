export TABLEVISION_API=https://ui2lc3zrbc.execute-api.ap-southeast-1.amazonaws.com/dev/tables
export GOOGLE_APPLICATION_CREDENTIALS="key.json"

DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/tablevision.py"