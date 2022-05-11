from curses import beep
from os import walk
import requests
import json

# Take project path

# Send to same project path

variables = []
for (dirpath, dirnames, filenames) in walk('./variables'):
        variables.extend(filenames)
        break

projects = []
for (dirpath, dirnames, filenames) in walk('./projects'):
        projects.extend(filenames)

new_projects = []
for (dirpath, dirnames, filenames) in walk('./new-projects'):
        new_projects.extend(filenames)

variables_id = []
for i in range(len(variables)):
        id = variables[i].split('-')
        variables_id.extend(id[0])

projects_id = []
for i in range(len(projects)):
        id = projects[i].split('-')
        projects_id.extend(id[0])

new_projects_id = []
for i in range(len(new_projects)):
        id = new_projects[i].split('-')
        projects_id.extend(id[0])

api = 'http://localhost:8080/api/v4/'

headers = {'PRIVATE-TOKEN' : 'sWQYxfYNJzbk4Mvksg61'}

def post():
        for i in variables:
                file = open(f'./variables/{i}', 'rb')
                data = json.loads(file.read())

        for i in projects:
                projects_files = open(f'./projects/{i}') 
                projects_content = json.loads(projects_files.read())
                
        for i in new_projects:
                new_projects_files = open(f'./new-projects/{i}')
                new_projects_content = json.loads(new_projects_files.read())

        
                for i in range(len(variables_id)):
                        try:
                                if variables_id[i] == projects_id[i]:
                                        if (projects_content[i]['path'] == new_projects_content[i]['path']):
                        
                                                for j in range(len(data)):
                                                                url = f"{api}projects/{new_projects_id[j]}/variables"
                                                                response = requests.post(url=url, data=data[j], headers=headers)
                                                                print(url)
                                                                print(response)
                        except KeyError:
                                break
                        
if __name__ == "__main__":
        post()