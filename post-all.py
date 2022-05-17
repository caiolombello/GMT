import subprocess
from colorama import Fore
from os import remove, walk, mkdir, path, environ
import requests
import json

ORIGIN_API = environ['ORIGIN_API']
ORIGIN_TOKEN = environ['ORIGIN_TOKEN']

headers = {'PRIVATE-TOKEN' : ORIGIN_TOKEN}

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
                        response = requests.post(url=ORIGIN_API+"/projects", data=data, headers=headers)
                        if response.status_code == 201:
                                print(Fore.GREEN + f"ID: {str(data['id'])}\t{str(response)}" + Fore.WHITE)
                                clone_repo_content(str(data['id']))
                        else:   
                                print(Fore.RED + 'ID: ' + str(data['id']) + '\t' + str(response))
                                files.remove(j)
                                continue
        write_post()
        push_repo_content()


def write_post():
        print(Fore.BLUE + '\nSAVING NEW PROJECTS')
        if not path.exists("new-projects"):
                mkdir("new-projects")
        response = requests.get(url=ORIGIN_API+'/projects?per_page=100', headers={'PRIVATE-TOKEN': f'{ORIGIN_TOKEN}'})        
        if response.status_code == 200:
                print(Fore.GREEN + str(response))
        else:
                print(Fore.RED + str(response))
        resp_dict = json.loads(response.content)
        for i in range(len(resp_dict)):
                filename = f"{resp_dict[i]['id']}-project.json"
                with open(f"./new-projects/{filename}", "w") as write_file:
                        json.dump(resp_dict[i], write_file, indent=4)
                print(Fore.GREEN + f'{filename} SAVED')

def clone_repo_content(id):
        if not path.exists('repo-content'):
                mkdir('repo-content')
        file = open(f'./projects/{id}-project.json', 'rb')
        data = json.loads(file.read())
        if not path.exists(str(data['path'])):
                mkdir('./repo-content/' + str(data['path']))
                git("clone", data['ssh_url_to_repo'], './repo-content/' + str(data['path']))

def push_repo_content():
        files = []
        for (dirpath, dirnames, filenames) in walk('./new-projects'):
                files.extend(filenames)
        for i in files:
                file = open(f'./new-projects/{i}', 'rb')
                data = json.loads(file.read())
                path = f"./repo-content/{data['path']}"
                subprocess.Popen(["git", "remote", "rename", "origin", "old-origin"], cwd=path)
                subprocess.Popen(["git", "remote", "add", "origin", f"{data['ssh_url_to_repo']}"], cwd=path)
                subprocess.Popen(["git", "push", "-u", "origin", "--all"], cwd=path)
                subprocess.Popen(["git", "push", "-u", "origin", "--tags"], cwd=path)

def delete_projects():
        print(Fore.BLUE + '\nDELETING PROJECTS')
        files = []
        for (dirpath, dirnames, filenames) in walk('./new-projects'):
                files.extend(filenames)
        for i in range(len(files)):
                remove('./new-projects/' + files[i])        
        response = requests.get(url=ORIGIN_API+'/projects?per_page=100', headers={'PRIVATE-TOKEN': f'{ORIGIN_TOKEN}'})
        print(Fore.GREEN + str(response))
        resp_dict = json.loads(response.content)
        for j in range(len(resp_dict)):
                print("ID: " + str(resp_dict[j]['id']))
                requests.delete(url=ORIGIN_API+f"projects/{resp_dict[j]['id']}", headers={'PRIVATE-TOKEN': f'{ORIGIN_TOKEN}'}) 
                if response.status_code != 200:
                        print(Fore.RED + str(response))
                else:
                        print(Fore.GREEN + str(response))

def post_variables():
        print(Fore.BLUE + '\nPOSTING VARIABLES')
        
        variables = []
        for (dirpath, dirnames, filenames) in walk('./variables'):
                variables.extend(filenames)
                variables.sort()

        projects = []
        for (dirpath, dirnames, filenames) in walk('./projects'):
                projects.extend(filenames)
                projects.sort()

        new_projects = []
        for (dirpath, dirnames, filenames) in walk('./new-projects'):
                new_projects.extend(filenames)
                new_projects.sort()
        
        origin_ids = []
        for i in range(len(variables)):
                origin_id = variables[i].split("-")
                origin_ids.append(origin_id[0])
                       
        project_path = []
        project_id = []
        for j in range(len(origin_ids)):        
                project_file = open(f'./projects/{origin_ids[j]}-project.json', 'rb')
                project_data = json.loads(project_file.read())
                project_path.append(project_data['path'])
                project_id.append(str(project_data['id']))
        print(project_path)

        new_project_path = []
        new_project_id = []
        for j in range(len(new_projects)):        
                new_project_file = open(f'./new-projects/{new_projects[j]}', 'rb')
                new_project_data = json.loads(new_project_file.read())
                new_project_path.append(new_project_data['path'])
                new_project_id.append(str(new_project_data['id']))
        print(new_project_path)

        for j in range(len(project_path)):
                variable_file = open(f'./variables/{origin_ids[j]}-ci_variables.json', 'rb')
                variable_data = json.loads(variable_file.read())
                try:
                        pos = new_project_path.index(project_path[j])
                except ValueError:
                        print(project_path[j] + ' not in list')
                        continue

                for k in range(len(variable_data)):
                        print(f'/{new_project_id[pos]}/variables')
                        print(variable_data[k])
                        response = requests.post(url=ORIGIN_API+f'projects/{new_project_id[pos]}/variables', data=variable_data[k], headers=headers)
                        print(response)

if __name__ == "__main__":
        post() 
        post_variables()
        push_repo_content()
        # delete_projects()       