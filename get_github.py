import requests

api_prefix = "https://api.github.com/"
prefix_cnt = len("https://github.com/")

def make_repo_request(url):
    return api_prefix + "repos/" + url[prefix_cnt::] + "/commits?sha=master"

def make_commit_request(url, commit_id):
    return api_prefix + "repos/" + url[prefix_cnt::] + "/commits/" + commit_id

def make_contribs_request(url):
    return api_prefix + "repos/" + url[prefix_cnt::] + "/contributors"

def get_repo(url, n):
    response = requests.get(make_repo_request(url))
    if not response:
        print('Bad')
        return
    contribs_response = requests.get(make_contribs_request(url)).json()
    if not contribs_response:
        print('Bad')
        return
    contribs = []
    contribs_number_commits = {}
    files_number_commits = {}
    for contrib in contribs_response:
        contribs.append(contrib["login"])
        contribs_number_commits[contrib["login"]] = 0

    response_json = response.json()
    i = 0
    max_commit = None
    max_commit_len = 0
    for commit in response_json:
        if (i == n - 1):
            break
        commit_id = commit['sha']
        commit_response = requests.get(make_commit_request(url, commit_id)).json()
        if not commit_response:
            print('Bad')
            return
        if "committer" in commit:
            if commit["committer"] and ("login" in commit["committer"]) and (commit["committer"]["login"]):
                login = commit["committer"]["login"]
                if (login in contribs_number_commits):
                    contribs_number_commits[login] += 1
        f = open(commit_id, "a")
        files_len_total = 0
        if ("files" in commit_response):
            for file in commit_response["files"]:
                if file['filename'] not in files_number_commits:
                    files_number_commits[file['filename']] = 0
                files_number_commits[file['filename']] += 1
                if ("patch" in file):
                    patch = file["patch"]
                    files_len_total += len(patch)
                    f.write(patch)
                    f.write("\n\n\n\n")
        f.close()
        if (files_len_total > max_commit_len):
            max_commit_len = files_len_total
            max_commit = commit
        i += 1
    contribs_number_result = sorted(contribs_number_commits, key=contribs_number_commits.get, reverse=True)
    if max_commit:
        if 'committer' in max_commit:
            if 'login' in max_commit['committer']:
                print('Max commit length: ' + str(max_commit_len) + ' from ' + max_commit['committer']['login'])
            elif 'name' in max_commit:
                print('Max commit length: ' + str(max_commit_len) + ' from ' + max_commit['committer']['name'])
            else:
                print('No committer for max_commit')
    print('Contrib statistics:')
    print(contribs_number_commits)
    print(contribs_number_result)
    print('Files statistics:')
    print(files_number_commits)

def main():
    #URL = "https://github.com/testerSunshine/12306"
    URL = input("Please input URL to repo\n")
    n = int(input("How many commits you want to process?\n"))
    get_repo(URL, n)

if __name__ == "__main__":
    main()