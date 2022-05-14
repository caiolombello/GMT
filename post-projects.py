import subprocess
from colorama import Fore
from os import remove, walk, mkdir, rmdir, path
import requests
import json

api = 'http://localhost:8080/api/v4/projects'
token = 'sWQYxfYNJzbk4Mvksg61'

headers = {'PRIVATE-TOKEN' : token}

def git(*args):
        return subprocess.check_call(['git'] + list(args))

def post():
        files = []
        for (dirpath, dirnames, filenames) in walk('./projects'):
                files.extend(filenames)
        print(Fore.BLUE + '\nPOSTING PROJECTS')
        for i in range(len(files)):
                for j in files:
                        file = open(f'./projects/{j}', 'rb')
                        data = json.loads(file.read())
                        response = requests.post(url=api, data=data, headers=headers)
                        if response.status_code == 201:
                                print(Fore.GREEN + 'ID: ' + str(data['id']) + '    ' + str(response) + Fore.WHITE)
                                clone_repo_content(str(data['id']))
                        else:   
                                print(Fore.RED + 'ID: ' + str(data['id']) + '    ' + str(response))
                                files.remove(j)
                                continue
        print(Fore.BLUE + '\nSAVING NEW PROJECTS')
        if not path.exists:
                mkdir("new-projects")
        write_post()


def write_post():
        response = requests.get(url=api+'?per_page=100', headers={'PRIVATE-TOKEN': f'{token}'})        
        if response.status_code == 200:
                print(Fore.GREEN + str(response))
        else:
                print(Fore.RED + str(response))
        resp_dict = json.loads(response.content)
        for i in range(len(resp_dict)):
                with open(f"./new-projects/{resp_dict[i]['id']}-project.json", "w") as write_file:
                        json.dump(resp_dict[i], write_file, indent=4)

def clone_repo_content(id):
        if not path.exists('repo-content'):
                mkdir('repo-content')
        file = open(f'./projects/{id}-project.json', 'rb')
        data = json.loads(file.read())
        if not path.exists(str(data['id'])):
                mkdir('./repo-content/' + str(data['id']))
                git("clone", data['ssh_url_to_repo'], './repo-content/' + str(data['id']))        

def delete_projects():
        print(Fore.BLUE + '\nDELETING PROJECTS')
        files = []
        for (dirpath, dirnames, filenames) in walk('./new-projects'):
                files.extend(filenames)
        for i in range(len(files)):
                remove('./new-projects/' + files[i])
        response = requests.get(url=api+'?per_page=100', headers={'PRIVATE-TOKEN': f'{token}'})
        print(Fore.GREEN + str(response))
        resp_dict = json.loads(response.content)
        for j in range(len(resp_dict)):
                print("ID: " + str(resp_dict[j]['id']))
                requests.delete(url=api+f"/{resp_dict[j]['id']}", headers={'PRIVATE-TOKEN': f'{token}'}) 
                if response.status_code != 200:
                        print(Fore.RED + str(response))
                else:
                        print(Fore.GREEN + str(response))   

if __name__ == "__main__":
        post()
        # delete_projects()
        