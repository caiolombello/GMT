from os import walk, mkdir, path, environ
from colorama import Fore
import requests
import json

OLD_ORIGIN_API = environ["OLD_ORIGIN_API"]
OLD_ORIGIN_TOKEN = environ["OLD_ORIGIN_TOKEN"]


def request_id(option):
    response = requests.get(
        f"{OLD_ORIGIN_API}{option}", headers={"PRIVATE-TOKEN": f"{OLD_ORIGIN_TOKEN}"}
    )
    content = response.content
    print(Fore.CYAN + str(response))
    resp_dict = json.loads(content)
    ids = []
    if response.status_code != 200:
        return ids
    print(Fore.BLUE + option)
    for i in range(len(resp_dict)):
        if "groups" in option and "variables" in option:
            prefix = option.split("/")
            if not path.exists("groups-variables"):
                mkdir("groups-variables")
            filename = f"{prefix[1]}-ci_variables.json"
            with open(f"./groups-variables/{filename}", "w") as write_file:
                json.dump(resp_dict, write_file, indent=4)
            print(Fore.GREEN + f"{filename} SAVED")
        elif "projects" in option and "variables" in option:
            prefix = option.split("/")
            if not path.exists("projects-variables"):
                mkdir("projects-variables")
            filename = f"{prefix[1]}-ci_variables.json"
            with open(f"./projects-variables/{filename}", "w") as write_file:
                json.dump(resp_dict, write_file, indent=4)
            print(Fore.GREEN + f"{filename} SAVED")
        elif "projects" in option:
            if resp_dict[i]["archived"] == True:
                continue
            if not path.exists("projects"):
                mkdir("projects")
            filename = f"{resp_dict[i]['id']}-project.json"
            with open(f"./projects/{filename}", "w") as write_file:
                json.dump(resp_dict[i], write_file, indent=4
                )
            print(Fore.GREEN + f"{filename} SAVED")
        elif "groups" in option:
            if not path.exists("groups"):
                mkdir("groups")
            filename = f"{resp_dict[i]['id']}-group.json"
            with open(f"./groups/{filename}", "w") as write_file:
                json.dump(resp_dict[i], write_file, indent=4)
            print(Fore.GREEN + f"{filename} SAVED")
            ids.append(resp_dict[i]["id"])
        else:
            ids.append(resp_dict[i]["id"])
    return ids

def projects_subgroups():
    print(Fore.YELLOW + "\nGROUPS")
    groups_ids = []
    for i in range(0, 20):
        option = f"/groups/{environ['SOURCE_ID']}/descendant_groups?page={i}"
        groups_ids.extend(request_id(option))
        print(Fore.WHITE + "IDS COUNT: " + str(len(groups_ids)))

    print(Fore.YELLOW + "\SUBGROUPS")
    for j in groups_ids:
        id = j
        option = f"groups/{id}/subgroups"
        groups_ids.extend(request_id(option))

    print(Fore.YELLOW + "\nPROJECTS")
    for j in groups_ids:
        id = j
        option = f"groups/{id}/projects/"
        print(Fore.LIGHTBLUE_EX + option)
        res = request_id(option)
        if res:
            groups_ids.extend(res)

    print(Fore.YELLOW + "\nUSERS")
    for i in groups_ids:
        option = f"groups/{i}/members/all?per_page=100"
        response = requests.get(
                f"{OLD_ORIGIN_API}{option}", headers={"PRIVATE-TOKEN": f"{OLD_ORIGIN_TOKEN}"}
            )
        content = response.content
        print(Fore.CYAN + str(response))
        resp_dict = json.loads(content)
        ids = []
        print(Fore.BLUE + option)
        if response.status_code != 200:
            print(Fore.RED + str(response))
        for j in range(len(resp_dict)):
            user = resp_dict[j]["username"]
            user = "".join([j for j in user if not j.isdigit()])
            if not path.exists("users"):
                mkdir("users")
            filename = f"{user}.json"
            with open(f"./users/{filename}", "w") as write_file:
                json.dump(
                    {
                        "username": user,
                        "name": resp_dict[j]["name"],
                        "email": f"{user}@vertigo.com.br",
                        "reset_password": "false",
                        "password": "V3rT1G0-D3v0P5-2022",
                        "skip_confirmation": "true"
                    },
                    write_file,
                    indent=4,
                )
                print(Fore.GREEN + f"{filename} SAVED")

def variables():
    print(Fore.YELLOW + "\nVARIABLES")

    projects_variables = []
    for (dirpath, dirnames, filenames) in walk("./projects"):
        projects_variables.extend(filenames)

    for j in projects_variables:
        file = open(f"./projects/{j}", "rb")
        data = json.loads(file.read())

        option = f"projects/{str(data['id'])}/variables"
        try:
            request_id(option)
        except:
            continue

    groups_variables = []
    for (dirpath, dirnames, filenames) in walk("./groups"):
        groups_variables.extend(filenames)

    for j in groups_variables:
        file = open(f"./groups/{j}", "rb")
        data = json.loads(file.read())

        option = f"groups/{str(data['id'])}/variables"
        try:
            request_id(option)
        except:
            continue


if __name__ == "__main__":
    projects_subgroups()
    variables()
