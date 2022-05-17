from os import walk, mkdir, environ, path
import requests
import json

# GET

OLD_ORIGIN_API = environ["OLD_ORIGIN_API"]
OLD_ORIGIN_TOKEN = environ["OLD_ORIGIN_TOKEN"]


def request(option):
    response = requests.get(
        f"{OLD_ORIGIN_API}{option}", headers={"PRIVATE-TOKEN": f"{OLD_ORIGIN_TOKEN}"}
    )
    content = response.content
    print(response)
    resp_dict = json.loads(content)
    ids = []
    print(option)
    if response.status_code != 200:
        print(response)
    for i in range(len(resp_dict)):
        user = resp_dict[i]["username"]
        user = "".join([i for i in user if not i.isdigit()])
        if not path.exists("users"):
            mkdir("users")
        with open(f"./users/{user}.json", "w") as write_file:
            json.dump(
                {
                    "username": user,
                    "name": resp_dict[i]["name"],
                    "email": f"{user}@vertigo.com.br",
                    "reset_password": "true",
                },
                write_file,
                indent=4,
            )


# POST

ORIGIN_API = environ["ORIGIN_API"]
ORIGIN_TOKEN = environ["ORIGIN_TOKEN"]

headers = {"PRIVATE-TOKEN": ORIGIN_TOKEN}


def post():
    files = []
    for (dirpath, dirnames, filenames) in walk("./users"):
        files.extend(filenames)

    for i in files:
        file = open(f"./users/{i}", "rb")
        data = json.loads(file.read())
        response = requests.post(url=ORIGIN_API+'/users', data=data, headers=headers)
        if response.status_code == 201:
            print("USER CREATED: " + data["username"])
        print(response)


if __name__ == "__main__":
    request(f"groups/{environ['SOURCE_ID']}/members")
    post()
