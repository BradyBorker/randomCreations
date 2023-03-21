import requests

# Get all groups in Jira
groups_url = "https://your-jira-instance.atlassian.net/rest/api/2/groups/picker"
groups_response = requests.get(groups_url, auth=('username', 'api_token'))
if groups_response.status_code == 200:
    groups = groups_response.json()["groups"]
else:
    print("Error retrieving groups:", groups_response.status_code, groups_response.text)
    exit()

# Loop through each group and determine which projects it is in
for group in groups:
    group_name = group["name"]
    projects_url = "https://your-jira-instance.atlassian.net/rest/api/2/groupuserpicker"
    projects_params = {"query": group_name, "showAvatar": True}
    projects_response = requests.get(projects_url, params=projects_params, auth=('username', 'api_token'))
    if projects_response.status_code == 200:
        results = projects_response.json()["users"]
        for result in results:
            if result["name"] == group_name:
                projects = result.get("projects", [])
                project_names = [project["name"] for project in projects]
                break
        else:
            print("Error: group", group_name, "not found in group user picker results")
            continue
    else:
        print("Error retrieving projects for group", group_name, ":", projects_response.status_code, projects_response.text)
        continue

    # Loop through each project and find out what permissions the group has been given
    for project_name in project_names:
        permissions_url = "https://your-jira-instance.atlassian.net/rest/api/2/project/" + project_name + "/permission"
        permissions_response = requests.get(permissions_url, auth=('username', 'api_token'))
        if permissions_response.status_code == 200:
            permissions = permissions_response.json()["permissions"]
            for permission in permissions:
                permission_name = permission["permission"]
                permission_description = permission["description"]
                print(group_name, "has permission", permission_name, "in project", project_name, "(", permission_description, ")")
        else:
            print("Error retrieving permissions for group", group_name, "in project", project_name, ":", permissions_response.status_code, permissions_response.text)
