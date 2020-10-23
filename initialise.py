import sys, json, requests

def main(table_json):
    endpoint = "http://18.139.111.67:5000/initialise"

    headers = {"content-type": "application/json"}

    # table_json = json.dumps(table_json)

    data = json.dumps({
        "tables_json": table_json
    })

    response = requests.post(endpoint, data=data, headers=headers)

    if response.ok:
        print('ok')
    else:
        print(response.text)


if __name__ == "__main__":
    table_json = sys.argv[1]
    main(table_json)
    