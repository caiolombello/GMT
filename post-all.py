from asyncore import write
import subprocess
from time import sleep
from colorama import Fore
from os import walk, mkdir, path, environ
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
    for i in files:
        file = open(f"./projects/{i}", "rb")
        data = json.loads(file.read())
        try:
            clone_repo_content(str(data["id"]))
        except:
            continue
    post_variables()
    edit_projects()

def request_id(option):
    response = requests.get(
            f"{ORIGIN_API}{option}", headers={"PRIVATE-TOKEN": f"{ORIGIN_TOKEN}"}
        )
    content = response.content
    print(Fore.CYAN + str(response))
    resp_dict = json.loads(content)
    ids = []
    if response.status_code != 200:
        return ids
    print(Fore.BLUE + option)
    for i in range(len(resp_dict)):
        if "groups" in option:
            if not path.exists("new-groups"):
                mkdir("new-groups")
            filename = f"{resp_dict[i]['id']}-group.json"
            with open(f"./new-groups/{filename}", "w") as write_file:
                json.dump(resp_dict[i], write_file, indent=4)
            print(Fore.GREEN + f"{filename} SAVED")
            ids.append(resp_dict[i]["id"])
        else:
            ids.append(resp_dict[i]["id"])
    return ids


def write_groups():
    print(Fore.YELLOW + "\nSAVING NEW GROUPS")
    groups_ids = []
    for i in range(0, 20):
        option = f"/groups/{environ['NEW_SOURCE_ID']}/descendant_groups?page={i}"
        groups_ids.extend(request_id(option))
        print(Fore.WHITE + "IDS COUNT: " + str(len(groups_ids)))

    print(Fore.YELLOW + "\SUBGROUPS")
    for j in groups_ids:
        id = j
        option = f"groups/{id}/subgroups"
        groups_ids.extend(request_id(option))

def write_projects():
    print(Fore.BLUE + "\nSAVING NEW PROJECTS")
    if not path.exists("new-projects"):
        mkdir("new-projects")
    for i in range(0, 50):
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
    local = f"./repo-content/{data['id']}"
    origin = str(data['http_url_to_repo']).replace('https://', '')
    link = origin.replace('gitlab.com', 'gitlab.vertigo-devops.com')
    time = 2
    if not path.exists(local):
        mkdir(local)
        print(Fore.YELLOW + str(data['path'] + Fore.WHITE))
        git("clone", "--mirror", f"https://{OLD_ORIGIN_USER}:{OLD_ORIGIN_TOKEN}@{origin}", local)
        sleep(time)
        subprocess.Popen(["git", "remote", "rename", "origin", "old-origin"], cwd=local)
        subprocess.Popen(
            ["git", "remote", "add", "origin", f"https://{ORIGIN_USER}:{ORIGIN_TOKEN}@{link}"], cwd=local
        )
        subprocess.Popen(["git", "push", "-u", "origin", "--mirror"], cwd=local)
        sleep(time)
    else:        
        print(Fore.YELLOW + str(data['path'] + Fore.WHITE))
        subprocess.Popen(["git", "pull"], cwd=local)
        sleep(time)
        subprocess.Popen(["git", "remote", "rename", "origin", "old-origin"], cwd=local)
        subprocess.Popen(
            ["git", "remote", "add", "origin", f"https://{ORIGIN_USER}:{ORIGIN_TOKEN}@{link}"], cwd=local
        )
        subprocess.Popen(["git", "push", "-u", "origin", "--mirror"], cwd=local)
        sleep(time)


def post_variables():
    write_projects()
    print(Fore.BLUE + "\nPOSTING PROJECTS VARIABLES")

    projects_variables = []
    for (dirpath, dirnames, filenames) in walk("./projects-variables"):
        projects_variables.extend(filenames)
        projects_variables.sort()

    projects = []
    for (dirpath, dirnames, filenames) in walk("./projects"):
        projects.extend(filenames)
        projects.sort()

    new_projects = []
    for (dirpath, dirnames, filenames) in walk("./new-projects"):
        new_projects.extend(filenames)
        new_projects.sort()

    origin_ids = []
    for i in range(len(projects_variables)):
        origin_id = projects_variables[i].split("-")
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
        try:
            variable_file = open(f"./projects-variables/{origin_ids[j]}-ci_variables.json", "rb")
            variable_data = json.loads(variable_file.read())
            pos = new_project_path.index(project_path[j])
        except ValueError:
            continue

        for k in range(len(variable_data)):
            print(f"/{new_project_id[pos]}/projects-variables")
            print(variable_data[k])
            response = requests.post(
                url=ORIGIN_API + f"projects/{new_project_id[pos]}/variables",
                data=variable_data[k],
                headers=headers,
            )
            print(response)

    write_groups()
    print(Fore.BLUE + "\nPOSTING GROUPS VARIABLES")

    groups_variables = []
    for (dirpath, dirnames, filenames) in walk("./groups-variables"):
        groups_variables.extend(filenames)
        groups_variables.sort()

    groups = []
    for (dirpath, dirnames, filenames) in walk("./groups"):
        groups.extend(filenames)
        groups.sort()

    new_groups = []
    for (dirpath, dirnames, filenames) in walk("./new-groups"):
        new_groups.extend(filenames)
        new_groups.sort()

    origin_ids = []
    for i in range(len(groups_variables)):
        origin_id = groups_variables[i].split("-")
        origin_ids.append(origin_id[0])

    group_path = []
    group_id = []
    for j in range(len(origin_ids)):
        group_file = open(f"./groups/{origin_ids[j]}-group.json", "rb")
        group_data = json.loads(group_file.read())
        group_path.append(group_data["path"])
        group_id.append(str(group_data["id"]))
    print(group_path)

    group_path = []
    new_group_id = []
    for j in range(len(new_groups)):
        new_group_file = open(f"./new-groups/{new_groups[j]}", "rb")
        new_group_data = json.loads(new_group_file.read())
        group_path.append(new_group_data["path"])
        new_group_id.append(str(new_group_data["id"]))
    print(group_path)

    for j in range(len(group_path)):
        try:
            variable_file = open(f"./groups-variables/{origin_ids[j]}-ci_variables.json", "rb")
            variable_data = json.loads(variable_file.read())
            pos = group_path.index(group_path[j])
        except:
            continue

        for k in range(len(variable_data)):
            print(f"/{new_group_id[pos]}/variables")
            print(variable_data[k])
            response = requests.post(
                url=ORIGIN_API + f"groups/{new_group_id[pos]}/variables",
                data=variable_data[k],
                headers=headers,
            )
            print(response)


def edit_projects():
    projects = []
    for (dirpath, dirnames, filenames) in walk("./projects"):
        projects.extend(filenames)

    new_projects = []
    for (dirpath, dirnames, filenames) in walk("./new-projects"):
        new_projects.extend(filenames)

    for i in range(len(new_projects)):
        new_file = open(f"./new-projects/{new_projects[i]}", "rb")
        new_data = json.loads(new_file.read())
        old_file = open(f"./projects/{projects[i]}", "rb")
        old_data = json.loads(old_file.read())
        
        if new_data["path_with_namespace"] == old_data["path_with_namespace"]:
            response = requests.put(url=ORIGIN_API+f'/projects/{new_data["id"]}', 
            data={
                "name": old_data["name"],
                "description": old_data["description"],
                "tag_list": old_data["tag_list"],
                "topics": old_data["topics"]
                }, 
                    headers=headers)
            print(new_data["name"])
            print(response)
        
            
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
