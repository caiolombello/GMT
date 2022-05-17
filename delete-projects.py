from colorama import Fore
from os import remove, walk, environ
import requests
import json

ORIGIN_API = environ['ORIGIN_API']
ORIGIN_TOKEN = environ['ORIGIN_TOKEN']

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

if __name__ == "__main__":
        delete_projects()     