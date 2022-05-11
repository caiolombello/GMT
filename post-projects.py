from os import walk
import requests
import json

api = 'http://localhost:8080/api/v4/projects'
token = 'sWQYxfYNJzbk4Mvksg61'

headers = {'PRIVATE-TOKEN' : token}
files = []
for (dirpath, dirnames, filenames) in walk('./projects'):
        files.extend(filenames)
        break

def post():
        for i in range(len(files)):
                try:
                        for j in files:
                                file = open(f'./projects/{j}', 'rb')
                                data = json.loads(file.read())
                                print(data['id'])
                                response = requests.post(url=api, data=data, headers=headers)
                                print(response)
                except KeyError:
                        continue

def write_post():
        response = requests.get(url=api, headers={'PRIVATE-TOKEN': f'{token}'})        
        print(response)
        resp_dict = json.loads(response.content)
        for i in range(len(resp_dict)):
                with open(f"./new-projects/{resp_dict[i]['id']}-project.json", "w") as write_file:
                        json.dump(resp_dict[i], write_file, indent=4)

def delete_projects():
        response = requests.get(url=api, headers={'PRIVATE-TOKEN': f'{token}'})        
        print(response)
        resp_dict = json.loads(response.content)
        for i in range(len(resp_dict)):
                if response.status_code != 200:
                        break
                print(f"{resp_dict[i]['id']}")
                requests.delete(url=api+f"/{resp_dict[i]['id']}", headers={'PRIVATE-TOKEN': f'{token}'}) 
                print(response)


if __name__ == "__main__":
        
