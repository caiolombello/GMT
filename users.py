from os import walk
import requests
import json

# GET

api = "https://gitlab.com/api/v4/"
get_token = 'glpat-Sa6G7btfkL6Vm-e7maAY'

def request(option):         
        response = requests.get(f"{api}{option}", headers={'PRIVATE-TOKEN': f'{get_token}'})        
        content = response.content
        print(response)
        resp_dict = json.loads(content)
        ids = []
        print(option)
        if response.status_code != 200:
                print(response)    
        for i in range(len(resp_dict)):
                with open(f"./users/{resp_dict[i]['id']}-user.json", "w") as write_file:
                        json.dump(resp_dict, write_file, indent=4)

# POST

url = 'http://localhost:8080/api/v4/users/'
post_token = 'sWQYxfYNJzbk4Mvksg61'

headers = {'PRIVATE-TOKEN' : post_token}
files = []
for (dirpath, dirnames, filenames) in walk('./users'):
        files.extend(filenames)
        break

def post():
        for i in files:
                file = open(f'./users/{i}', 'rb')
                data = json.loads(file.read())

                for i in range(len(data)):
                        response = requests.post(url=url, data=data[i], headers=headers)
                        print(url)
                        print(response)

if __name__ == "__main__":
        #request('users')
        post()
