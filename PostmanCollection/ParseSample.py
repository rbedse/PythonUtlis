import json

input_path = "./data/Sample.postman_collection.json"
output_path = "./data/Sample_R.json"

def get_baseurl_action(header: list):
    data = {d['key']: d['value'] for d in header}
    return data['origin']

def get_request_body_str(data: list):
    data = [json.dumps({d["key"]: d["value"]}).removeprefix('{').removesuffix('}') for d in data]
    data_str = '{' + ', '.join(data).replace("\"", "'") + '}'
    return data_str


# Open the JSON file and load its contents into a variable=
with open(input_path, "r") as file:
    data = json.load(file)

# Now, 'data' contains the contents of the JSON file as a Python dictionary
#print(data)
items = data['item']
#print(items)
expected_output = []

for item in items:
    new_item = {'TEST_NAMES': item['name']}
    url = item['request']['url']
    base_uri = get_baseurl_action(item['request']['header'])
    new_item['BASEURL_ACTION'] = base_uri
    new_item['DEPENDENT_FLAG'] = str(False)
    new_item['DEPENDENT_FLAG_COUNT'] = 0
    new_item['TEST_DATA'] = {
        "RELATIVE_URI": url.removeprefix(base_uri),
        "REQUEST_TYPE": item['request']['method'],
        "EXCEPTED_RESPONSE_STATUS": "200",
        "RESPONSE_BODY": '',
        "RESPONSE_BODY_EXACT_MATCH": str(False),
        "RESPONSE_BODY_CASE_SENSITIVE": str(False),
        "RESPONSE_BODY_START_WITH": "{'status': 'SUCCESS'",
        "RESPONSE_BODY_END_WITH": "}}}",
        "RESPONSE_BODY_CONTAINS": "'label': 'Peer Review'",
        "REQUEST_BODY":  get_request_body_str(item['request']['body']['urlencoded']),
        "DEPENDENT_VALUES": "",
        "ATTACHMENT": "NA"
        }
    expected_output.append(new_item)

with open(output_path, "w") as file:
    json.dump(expected_output, file, indent=4)

# print(json.dumps(expected_output))

# Open the file for reading
with open(output_path, "r") as file:
    content = file.read()

# Perform the replacement
modified_content = content.replace('\\\\', '\\')

# Open the file for writing with the modified content
with open(output_path, "w") as file:
    file.write(modified_content)
