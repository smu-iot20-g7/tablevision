export CLARIFAI_SECRET=
export TELEGRAM_KEY=
export PI_IPV4=192.168.1.74
export TABLEVISION_API=http://localhost:5000/tables
#export TABLEVISION_API=https://ui2lc3zrbc.execute-api.ap-southeast-1.amazonaws.com/dev/tables
DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/tablevision.py"