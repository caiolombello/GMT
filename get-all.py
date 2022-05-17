from os import walk, mkdir, path, environ
from colorama import Fore
import requests
import json

OLD_ORIGIN_API = environ['OLD_ORIGIN_API']
OLD_ORIGIN_TOKEN = environ['OLD_ORIGIN_TOKEN']

def request_id(option):         
        response = requests.get(f"{OLD_ORIGIN_API}{option}", headers={'PRIVATE-TOKEN': f'{OLD_ORIGIN_TOKEN}'})        
        content = response.content
        print(Fore.CYAN + str(response))
        resp_dict = json.loads(content)
        ids = []
        if response.status_code != 200:
                return ids
        print(Fore.BLUE + option)
        for i in range(len(resp_dict)):
                if 'subgroups' in option:
                        if not path.exists('subgroups'):
                                mkdir('subgroups')
                        filename = f"{resp_dict[i]['id']}-subgroup.json"
                        with open(f"./subgroups/{filename}", "w") as write_file:
                                json.dump(resp_dict[i], write_file, indent=4)
                        print(Fore.GREEN + f'{filename} SAVED')
                        ids.append(resp_dict[i]['id'])
                elif 'variables' in option:
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
                        if resp_dict[i]['archived'] == True:
                                continue
                        if not path.exists('projects'):
                                mkdir('projects')
                        filename = f"{resp_dict[i]['id']}-project.json"
                        with open(f"./projects/{filename}", "w") as write_file:
                                json.dump({
                                        'id':resp_dict[i]['id'],
                                        'name': resp_dict[i]['name'],
                                        'path': resp_dict[i]['path'],
                                        'allow_merge_on_skipped_pipeline': resp_dict[i]['allow_merge_on_skipped_pipeline'],
                                        'analytics_access_level': resp_dict[i]['analytics_access_level'],
                                        'auto_cancel_pending_pipelines': resp_dict[i]['auto_cancel_pending_pipelines'],
                                        'auto_devops_deploy_strategy': resp_dict[i]['auto_devops_deploy_strategy'],
                                        'auto_devops_enabled': resp_dict[i]['auto_devops_enabled'],
                                        'autoclose_referenced_issues': resp_dict[i]['autoclose_referenced_issues'],
                                        'avatar_url': resp_dict[i]['avatar_url'],
                                        'build_timeout': resp_dict[i]['build_timeout'],
                                        'builds_access_level': resp_dict[i]['builds_access_level'],
                                        'ci_config_path': resp_dict[i]['ci_config_path'],
                                        'container_registry_access_level': resp_dict[i]['container_registry_access_level'],
                                        'container_registry_enabled': resp_dict[i]['container_registry_enabled'],
                                        'default_branch': resp_dict[i]['default_branch'],
                                        'description': resp_dict[i]['description'],
                                        'emails_disabled': resp_dict[i]['emails_disabled'],
                                        'external_authorization_classification_label': resp_dict[i]['external_authorization_classification_label'],
                                        'forking_access_level': resp_dict[i]['forking_access_level'],
                                        'import_url': resp_dict[i]['import_url'],
                                        'issues_access_level': resp_dict[i]['issues_access_level'],
                                        'issues_enabled': resp_dict[i]['issues_enabled'],
                                        'jobs_enabled': resp_dict[i]['jobs_enabled'],
                                        'lfs_enabled': resp_dict[i]['lfs_enabled'],
                                        'merge_method': resp_dict[i]['merge_method'],
                                        'merge_requests_access_level': resp_dict[i]['merge_requests_access_level'],
                                        'merge_requests_enabled': resp_dict[i]['merge_requests_enabled'],
                                        'only_allow_merge_if_all_discussions_are_resolved': resp_dict[i]['only_allow_merge_if_all_discussions_are_resolved'],
                                        'only_allow_merge_if_pipeline_succeeds': resp_dict[i]['only_allow_merge_if_pipeline_succeeds'],
                                        'operations_access_level': resp_dict[i]['operations_access_level'],
                                        'packages_enabled': resp_dict[i]['packages_enabled'],
                                        'pages_access_level': resp_dict[i]['pages_access_level'],
                                        'printing_merge_request_link_enabled': resp_dict[i]['printing_merge_request_link_enabled'],
                                        'remove_source_branch_after_merge': resp_dict[i]['remove_source_branch_after_merge'],
                                        'repository_access_level': resp_dict[i]['repository_access_level'],
                                        'request_access_enabled': resp_dict[i]['request_access_enabled'],
                                        'requirements_access_level': resp_dict[i]['requirements_access_level'],
                                        'resolve_outdated_diff_discussions': resp_dict[i]['resolve_outdated_diff_discussions'],
                                        'security_and_compliance_access_level': resp_dict[i]['security_and_compliance_access_level'],
                                        'shared_runners_enabled': resp_dict[i]['shared_runners_enabled'],
                                        'snippets_access_level': resp_dict[i]['snippets_access_level'],
                                        'snippets_enabled': resp_dict[i]['snippets_enabled'],
                                        'squash_option': resp_dict[i]['squash_option'],
                                        'tag_list': resp_dict[i]['tag_list'],
                                        'topics': resp_dict[i]['topics'],
                                        'visibility': resp_dict[i]['visibility'],
                                        'wiki_access_level': resp_dict[i]['wiki_access_level'],
                                        'wiki_enabled': resp_dict[i]['wiki_enabled'],
                                        'ssh_url_to_repo': resp_dict[i]['ssh_url_to_repo'],
                                        'http_url_to_repo': resp_dict[i]['http_url_to_repo']
                                        }, write_file, indent=4)
                        print(Fore.GREEN + f'{filename} SAVED')
                else:
                        ids.append(resp_dict[i]['id'])
        return ids

def projects_main():
        print(Fore.YELLOW + "\nMAIN")
        id = '636953'
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
        print(Fore.YELLOW + "\nVARIABLES")
        
        files = []
        for (dirpath, dirnames, filenames) in walk('./projects'):
                files.extend(filenames)

        for j in files:
                file = open(f'./projects/{j}', 'rb')
                data = json.loads(file.read())

                option = f"projects/{str(data['id'])}/variables"
                request_id(option)

def runners():
        print(Fore.YELLOW + "\nRUNNERS")
        
        files = []
        for (dirpath, dirnames, filenames) in walk('./projects'):
                files.extend(filenames)

        for j in files:
                file = open(f'./projects/{j}', 'rb')
                data = json.loads(file.read())

                option = f"projects/{str(data['id'])}/runners"
                request_id(option)

if __name__ == "__main__":
        projects_subgroups()
        projects_ci()
        runners()