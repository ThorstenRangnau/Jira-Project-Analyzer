from github import Github, GithubException
from .github_access_keys import GITHUB_ACCESS_KEYS


def create_github_instances(repository_name):
    github_dict = dict()
    id_count = 0
    for access_key in GITHUB_ACCESS_KEYS:
        github_dict[id_count] = GitHubInstance(id_count, access_key, repository_name)
        id_count += 1
    return github_dict


class GitHubInstance:

    def __init__(self, id, access_key, repo):
        self.id = id
        github_instance = Github(access_key)
        self.repo = github_instance.get_repo(repo)
        self.requests = 1

    def get_commit(self, commit_sha):
        self.requests += 1
        return self.repo.get_commit(commit_sha)


class GitHubCommitService:

    def __init__(self, github_repository_name):
        self.github_instances = create_github_instances(github_repository_name)
        self.current_instance_id = [*self.github_instances][0] # sets current instance to the first

    def get_commit(self, commit_sha):
        # TODO: check for requests of instance
        return self.github_instances[self.current_instance_id].get_commit(commit_sha)
