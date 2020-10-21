export CLARIFAI_SECRET=c070f2fab3e0444782327e22d5e9bb46
export PI_IPV4=192.168.1.74
# export TABLEVISION_API=http://localhost:5000/tables
export TABLEVISION_API=https://ui2lc3zrbc.execute-api.ap-southeast-1.amazonaws.com/dev/tables
export GOOGLE_APPLICATION_CREDENTIALS="key.json"

export API_SECRET=${gcloud auth application-default print-access-token}

DIR="$( cd "$( dirname "$0" )" && pwd )"
alias python=python3
python "$DIR/tablevision_v1.py"