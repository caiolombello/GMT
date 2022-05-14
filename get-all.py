from os import remove, walk, mkdir, rmdir, path, listdir
from colorama import Fore
import requests
import json

api = "https://gitlab.com/api/v4/"
token = 'glpat-Sa6G7btfkL6Vm-e7maAY'

def request_id(option):         
        response = requests.get(f"{api}{option}", headers={'PRIVATE-TOKEN': f'{token}'})        
        content = response.content
        print(Fore.CYAN + str(response))
        resp_dict = json.loads(content)
        ids = []
        if response.status_code != 200:
                return ids
        print(Fore.BLUE + option)
        for i in range(len(resp_dict)):
                if 'variables' in option:
                        prefix = option.split("/")
                        if not path.exists('variables'):
                                mkdir('variables')
                        filename = f"{prefix[1]}-ci_variables.json"
                        with open(f"./variables/{filename}", "w") as write_file:
                                json.dump(resp_dict, write_file, indent=4)
                        print(Fore.GREEN + f'{filename} SAVED')
                elif 'runners' in option:
                        if not path.exists('runners'):
                                mkdir('runners')
                        filename = f"{resp_dict[i]['id']}-runner.json"
                        with open(f"./runners/{filename}", "w") as write_file:
                                if json.dump(resp_dict[i], write_file, indent=4):
                                        print(Fore.GREEN + f'{filename} SAVED')
                elif 'projects' in option:
                        if not path.exists('projects'):
                                mkdir('projects')
                        filename = f"{resp_dict[i]['path']}.json"
                        with open(f"./projects/{filename}", "w") as write_file:
                                json.dump(resp_dict[i], write_file, indent=4)
                        print(Fore.GREEN + f'{filename} SAVED')
                else:
                        ids.append(resp_dict[i]['id'])
        return ids

def projects_main():
        print(Fore.YELLOW + "\nMAIN")
        id = '3544756'
        option = f'groups/{id}/subgroups'
        
        ids = request_id(option)
        main = []
        for i in ids:
                id = i
                option = f'groups/{id}/subgroups'
                main.extend(request_id(option))
        print("OK")
        
        print(Fore.YELLOW + "\nMAIN PROJECTS")
        project = []
        for i in ids:
                id = i
                option = f'groups/{id}/projects/'
                print(Fore.LIGHTBLUE_EX + option)
                res = request_id(option)
                if res:
                        project.extend(res)
        print("OK")
        print(Fore.WHITE + 'TOOK IDS: ' + str(main))
        return main

def projects_groups():
        print(Fore.YELLOW + "\nGROUPS")
        groups_ids = projects_main()
        for i in groups_ids:
                id = i
                option = f'groups/{id}/subgroups'
                groups_ids.extend(request_id(option))

        
        print(Fore.YELLOW + "\nGROUP PROJECTS")
        for i in groups_ids:
                id = i
                option = f'groups/{id}/projects/'
                print(Fore.LIGHTBLUE_EX + option)
                res = request_id(option)
                if res:
                        groups_ids.extend(res)
        print("OK")
        print(Fore.WHITE + 'TOOK IDS: ' + str(groups_ids))
        return groups_ids

def projects_subgroups():
        print(Fore.YELLOW + "\nSUBGROUPS")
        groups_ids = projects_groups()
        for i in groups_ids:
                id = i
                option = f'groups/{id}/subgroups'
                groups_ids.extend(request_id(option))

        
        print(Fore.YELLOW + "\nSUBGROUP PROJECTS")
        for i in groups_ids:
                id = i
                option = f'groups/{id}/projects/'
                print(Fore.LIGHTBLUE_EX + option)
                res = request_id(option)
                if res:
                        groups_ids.extend(res)
        print("OK")
        print(Fore.WHITE + 'TOOK IDS: ' + str(groups_ids))
        print(Fore.WHITE + 'IDS COUNT: ' + str(len(groups_ids)))
        return groups_ids

def projects_ci():
        print(Fore.YELLOW + "VARIABLES")
        
        files = []
        for (dirpath, dirnames, filenames) in walk('./projects'):
                files.extend(filenames)

        for j in files:
                file = open(f'./projects/{j}', 'rb')
                data = json.loads(file.read())

                option = f"projects/{str(data['id'])}/variables"
                request_id(option)

def runners():
        print(Fore.YELLOW + "RUNNERS")
        
        files = []
        for (dirpath, dirnames, filenames) in walk('./projects'):
                files.extend(filenames)

        for j in files:
                file = open(f'./projects/{j}', 'rb')
                data = json.loads(file.read())

                option = f"projects/{str(data['id'])}/runners"
                request_id(option)

if __name__ == "__main__":
        # projects_subgroups()
        # projects_ci()
        runners()