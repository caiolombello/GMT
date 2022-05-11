import requests
import json

api = "https://gitlab.com/api/v4/"
token = 'glpat-Sa6G7btfkL6Vm-e7maAY'

def request_id(option):         
        response = requests.get(f"{api}{option}", headers={'PRIVATE-TOKEN': f'{token}'})        
        content = response.content
        print(response)
        resp_dict = json.loads(content)
        ids = []
        print(option)
        if response.status_code != 200:
                return ids    
        for i in range(len(resp_dict)):
                if 'variables' in option:
                        prefix = option.split("/")
                        with open(f"./variables/{prefix[2]}-ci_variables.json", "w") as write_file:
                                json.dump(resp_dict, write_file, indent=4)
                else:
                        ids.append(resp_dict[i]['id'])
        return ids

def projects_main():
        print("MAIN")
        id = '3544756'
        option = f'groups/{id}/subgroups'
        
        ids = request_id(option)
        main = []
        for i in ids:
                id = i
                option = f'groups/{id}/subgroups'
                main.extend(request_id(option))
        print("OK")
        
        print("MAIN PROJECTS")
        project = []
        for i in ids:
                id = i
                option = f'groups/{id}/projects/'
                print(option)
                res = request_id(option)
                if res:
                        project.extend(res)
        print("OK")
        return main

def projects_groups():
        ids = projects_main()
        print("GROUPS")
        groups = projects_main()
        for i in ids:
                id = i
                option = f'groups/{id}/subgroups'
                groups.extend(request_id(option))

        
        print("GROUP PROJECTS")
        project = projects_main()
        for i in ids:
                id = i
                option = f'groups/{id}/projects/'
                print(option)
                res = request_id(option)
                if res:
                        project.extend(res)
        print("OK")
        return groups

def projects_subgroups():
        ids = projects_groups()
        print("SUBGROUPS")
        groups = []
        for i in ids:
                id = i
                option = f'groups/{id}/subgroups'
                groups.extend(request_id(option))

        
        print("SUBGROUP PROJECTS")
        project = []
        for i in ids:
                id = i
                option = f'groups/{id}/projects/'
                print(option)
                res = request_id(option)
                if res:
                        project.extend(res)
        print("OK")
        return project

def projects_ci(ids):
        print("VARIABLES")
        variables = []
        for i in ids:
                id = i
                option = f'/projects/{id}/variables'
                print(option)
                variables.extend(request_id(option))
        print("OK")
        return variables

if __name__ == "__main__":
        projects_ci(projects_subgroups()) 
