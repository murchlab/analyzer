# import worker
import os
import base64
import json

dict_data = {'module': 'test_module.py', 'function': 'rand', 'arguments': [{'0': 'n', '1': 2}]}
json_data = json.dumps(dict_data)

json_data_bytes = json_data.encode('utf-8')
base64_bytes = base64.b64encode(json_data_bytes)
base64_message = base64_bytes.decode('utf-8')

# print(base64_message)

os.system("python worker.py " + base64_message)
# worker.main(json_data)