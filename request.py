import requests
import json

api = "https://gitlab.com/api/v4/"
token = input("token: ") # glpat-Sa6G7btfkL6Vm-e7maAY
target_api = input("api to import from gitlab: ")
option = input("""Options:
1) Export Users
2) Export Projects
3) Export Subgroups
4) Export Groups
5) Export CI Variables
6) Export Runners
""")

def request(option):         
        response = requests.get(f"{api}{option}", headers={'PRIVATE-TOKEN': f'{token}'})        
        content = response.content
        print(response)
        resp_dict = json.loads(content)
        ids = []
        print(option)
        if response.status_code == 404:
                return ids    
        for i in range(len(resp_dict)):
                ids.append(resp_dict[i]['id'])
        return ids

def users():
        option = 'users'
        return option

def projects():
        print("PROJECTS")
        ids = request(subgroups())
        project = []
        for i in ids:
                id = i
                option = f'groups/{id}/projects/'
                print(option)
                if request(option):
                        project.append(request(option))
        print(project)

def groups():
        option = 'groups'
        return option

def subgroups():
        print("SUBGROUPS")
        id = '3544756'
        option = f'groups/{id}/subgroups'
        
        ids = request(option)
        subgroup = []
        for i in ids:
                id = i
                if request(option):
                        subgroup.append(request(option))

        group = []
        for i in subgroup:
                if i not in group:
                        group.append(i)
        print("OK")
        return id

def variables():
        option = 'projects/{id}/variables'
        return option

def runners():
        option = 'projects/{id}/runners'
        return option

if __name__ == "__main__":

        if option == "1":
                option = request(users())
        elif option == "2":
                option = request(projects())
        elif option == "3":
                options = request(subgroups())
        elif option == "4":
                option = request(groups())
        elif option == "5":
                option = request(variables())
        elif option == "6":
                option = request(runners())
        else:
                print("Invalid option")

        
        


