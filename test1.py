li = [{'personName': 'oil', 'personId': '41f3c76d-5bee-418b-8f65-5233b3521789'}, 
      {'personName': 'golf', 'personId': '506ec04e-8a43-4e44-9843-2a411ab36146'}, 
      {'personName': 'sprite', 'personId': '7f96cced-fe6c-4ed4-8332-33a0c36f6aeb'}, 
      {'personName': 'gene', 'personId': 'd30f428e-0a15-4eb5-9f07-d5886dd5a574'}, 
      {'personName': 'ice', 'personId': 'f29d819f-8b24-4bb6-bd17-055bc64ed32c'}]

functions = [{'describe': 'Open Camera', 'function_name': 'open_camera'},
             {'describe': 'Azure Camera', 'function_name': 'azure_camera'},
             {'describe': 'List Group', 'function_name': 'list_group'},
             {'describe': 'List person', 'function_name': 'list_person'},
             {'describe': 'Create Group', 'function_name': 'create_group'},
             {'describe': 'Create Person Group', 'function_name': 'create_person_group'},
             {'describe': 'Detection', 'function_name': 'detection'},
             {'describe': 'Sync Person', 'function_name': 'sync_person'},
             {'describe': 'Quit', 'function_name': 'quit'}]

print(li[0])
print(li[0]['personName'])

def open_camera():
    print('open camera')


def azure_camera():
    print('azure_camera')


for i in range(len(functions)):
    print("\t"+str(i+1)+". "+str(functions[i]['describe']))


select = input('Select: ')

if str(select).isdigit() and int(select) >= 0 and int(select) <= len(functions):
    locals()[functions[int(select)-1]['function_name']]()
else:
    print("Please input number in range only")