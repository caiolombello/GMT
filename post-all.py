from asyncore import write
import subprocess
from time import sleep
from colorama import Fore
from os import remove, walk, mkdir, path, environ
import requests
import json

OLD_ORIGIN_USER = environ["OLD_ORIGIN_USER"]
OLD_ORIGIN_TOKEN = environ["OLD_ORIGIN_TOKEN"]
ORIGIN_USER = environ["ORIGIN_USER"]
ORIGIN_TOKEN = environ["ORIGIN_TOKEN"]
ORIGIN_API = environ["ORIGIN_API"]


headers = {"PRIVATE-TOKEN": ORIGIN_TOKEN}


def git(*args):
    return subprocess.check_call(["git"] + list(args))

def post_projects():
    files = []
    for (dirpath, dirnames, filenames) in walk("./projects"):
        files.extend(filenames)
    print(Fore.BLUE + "\nPOSTING PROJECTS")
    for i in range(len(files)):
        for j in files:
            file = open(f"./projects/{j}", "rb")
            data = json.loads(file.read())
            clone_repo_content(str(data["id"]))
    write_post()
    post_variables()

def write_post():
    print(Fore.BLUE + "\nSAVING NEW PROJECTS")
    if not path.exists("new-projects"):
        mkdir("new-projects")
    for i in range(0, 20):
        response = requests.get(
            url=ORIGIN_API + f"/projects?page={i}",
            headers={"PRIVATE-TOKEN": f"{ORIGIN_TOKEN}"}
        )
        if response.status_code == 200:
            print(Fore.GREEN + str(response))
        else:
            print(Fore.RED + str(response))
        resp_dict = json.loads(response.content)
        for i in range(len(resp_dict)):
            filename = f"{resp_dict[i]['id']}-project.json"
            with open(f"./new-projects/{filename}", "w") as write_file:
                json.dump(resp_dict[i], write_file, indent=4)
            print(Fore.GREEN + f"{filename} SAVED")


def clone_repo_content(id):
    if not path.exists("repo-content"):
        mkdir("repo-content")
    file = open(f"./projects/{id}-project.json", "rb")
    data = json.loads(file.read())
    local = f"./repo-content/{data['path']}"
    origin = str(data['http_url_to_repo']).replace('https://', '')
    link = origin.replace('gitlab.com', 'gitlab.vertigo-devops.com')
    time = 5
    if not path.exists(local):
        mkdir(local)
        git("clone", f"https://{OLD_ORIGIN_USER}:{OLD_ORIGIN_TOKEN}@{origin}", local)
        sleep(time)
        subprocess.Popen(["git", "remote", "rename", "origin", "old-origin"], cwd=local)
        sleep(time)
        subprocess.Popen(
            ["git", "remote", "add", "origin", f"https://{ORIGIN_USER}:{ORIGIN_TOKEN}@{link}"], cwd=local
        )
        sleep(time)
        subprocess.Popen(["git", "push", "-u", "origin", "--all"], cwd=local)
        sleep(time)
        subprocess.Popen(["git", "push", "-u", "origin", "--tags"], cwd=local)
        sleep(time)
    else:        
        subprocess.Popen(["git", "remote", "rename", "origin", "old-origin"], cwd=local)
        sleep(time)
        subprocess.Popen(
            ["git", "remote", "add", "origin", f"https://{ORIGIN_USER}:{ORIGIN_TOKEN}@{link}"], cwd=local
        )
        sleep(time)
        subprocess.Popen(["git", "push", "-u", "origin", "--all"], cwd=local)
        sleep(time)
        subprocess.Popen(["git", "push", "-u", "origin", "--tags"], cwd=local)
        sleep(time)


def post_variables():
    print(Fore.BLUE + "\nPOSTING VARIABLES")

    variables = []
    for (dirpath, dirnames, filenames) in walk("./variables"):
        variables.extend(filenames)
        variables.sort()

    projects = []
    for (dirpath, dirnames, filenames) in walk("./projects"):
        projects.extend(filenames)
        projects.sort()

    new_projects = []
    for (dirpath, dirnames, filenames) in walk("./new-projects"):
        new_projects.extend(filenames)
        new_projects.sort()

    origin_ids = []
    for i in range(len(variables)):
        origin_id = variables[i].split("-")
        origin_ids.append(origin_id[0])

    project_path = []
    project_id = []
    for j in range(len(origin_ids)):
        project_file = open(f"./projects/{origin_ids[j]}-project.json", "rb")
        project_data = json.loads(project_file.read())
        project_path.append(project_data["path"])
        project_id.append(str(project_data["id"]))
    print(project_path)

    new_project_path = []
    new_project_id = []
    for j in range(len(new_projects)):
        new_project_file = open(f"./new-projects/{new_projects[j]}", "rb")
        new_project_data = json.loads(new_project_file.read())
        new_project_path.append(new_project_data["path"])
        new_project_id.append(str(new_project_data["id"]))
    print(new_project_path)

    for j in range(len(project_path)):
        variable_file = open(f"./variables/{origin_ids[j]}-ci_variables.json", "rb")
        variable_data = json.loads(variable_file.read())
        try:
            pos = new_project_path.index(project_path[j])
        except ValueError:
            print(project_path[j] + " not in list")
            continue

        for k in range(len(variable_data)):
            print(f"/{new_project_id[pos]}/variables")
            print(variable_data[k])
            response = requests.post(
                url=ORIGIN_API + f"projects/{new_project_id[pos]}/variables",
                data=variable_data[k],
                headers=headers,
            )
            print(response)


def write_groups():
    print(Fore.BLUE + "\nSAVING NEW GROUPS")
    if not path.exists("new-groups"):
        mkdir("new-groups")
    for i in range(0, 20):
        response = requests.get(
            url=ORIGIN_API + f"/groups/{environ['NEW_SOURCE_ID']}/descendant_groups?page={i}",
            headers={"PRIVATE-TOKEN": f"{ORIGIN_TOKEN}"},
        )
        if response.status_code == 200:
            print(Fore.GREEN + str(response))
        else:
            print(Fore.RED + str(response))
        resp_dict = json.loads(response.content)
        for i in range(len(resp_dict)):
            filename = f"{resp_dict[i]['path']}.json"
            with open(f"./new-groups/{filename}", "w") as write_file:
                json.dump(resp_dict[i], write_file, indent=4)
            print(Fore.GREEN + f"{filename} SAVED")


def transfer_projects():
    print(Fore.BLUE + "\nTRANSFERING PROJECTS TO GROUPS")
    groups = []
    for (dirpath, dirnames, filenames) in walk("./new-groups"):
        groups.extend(filenames)

    projects = []
    for (dirpath, dirnames, filenames) in walk("./projects"):
        projects.extend(filenames)

    projects_path = []
    projects_id = []
    for i in projects:
        project_file = open(f"./projects/{i}", "rb")
        project_data = json.loads(project_file.read())
        path = str(project_data['http_url_to_repo'])
        path = path.split('/')
        projects_path = path[-2]

        response_id = requests.get(
            url=ORIGIN_API + f"/projects?search={project_data['path']}",
            headers={"PRIVATE-TOKEN": f"{ORIGIN_TOKEN}"}
        )
        content = response_id.content
        resp_dict = json.loads(content)

        group_file = open(f"./new-groups/{projects_path}.json")
        group_data = json.loads(group_file.read())
        group_id = group_data['id']

        try:
            response = requests.post(
                url=ORIGIN_API + f"/groups/{group_id}/projects/{resp_dict[0]['id']}",
                headers={"PRIVATE-TOKEN": f"{ORIGIN_TOKEN}"}
            )
            if response.status_code == 201:
                print(Fore.GREEN + str(response))
            else:
                print(Fore.RED + str(response))
        except:
            continue


def post_users():
    files = []
    for (dirpath, dirnames, filenames) in walk("./users"):
        files.extend(filenames)

    for i in files:
        file = open(f"./users/{i}", "rb")
        data = json.loads(file.read())
        response = requests.post(url=ORIGIN_API+'/users', data=data, headers=headers)
        if response.status_code == 201:
            print(Fore.BLUE + "USER CREATED: " + data["username"])
        print(response)


if __name__ == "__main__":
    post_projects()
    post_users()