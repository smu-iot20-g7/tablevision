parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

export GOOGLE_APPLICATION_CREDENTIALS="$parent_path/key.json"

python3 predict.py