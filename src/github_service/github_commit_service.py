from github import Github, GithubException
from .github_access_keys import GITHUB_ACCESS_KEYS

RATE_LIMIT = 4990  # rate limit is 5000 but a little buffer may be nice!


def create_github_instances(repository_name):
    github_dict = dict()
    id_count = 0
    for access_key in GITHUB_ACCESS_KEYS:
        github_dict[id_count] = GitHubInstance(id_count, access_key, repository_name)
        id_count += 1
    return github_dict


class GitHubCommitServiceException(Exception):

    def __init__(self, message):
        self.message = message


class GitHubInstance:

    def __init__(self, id, access_key, repo):
        self.id = id
        github_instance = Github(access_key)
        self.repo = github_instance.get_repo(repo)
        self.requests = 1
        self.exceed_rate_limit = False

    def get_commit(self, commit_sha):
        self.check_rate_limit()
        self.requests += 1
        return self.repo.get_commit(commit_sha)

    def check_rate_limit(self):
        # if requests are 4989 we can perform the current but not the next
        if self.requests >= RATE_LIMIT - 1:
            self.exceed_rate_limit = True


class GitHubCommitService:

    def __init__(self, github_repository_name):
        self.github_instances = create_github_instances(github_repository_name)
        self.current_instance_id = [*self.github_instances][0] # sets current instance to the first

    def get_commit(self, commit_sha):
        self.check_instances()
        return self.github_instances[self.current_instance_id].get_commit(commit_sha)

    def check_instances(self):
        # check if we can still use the current instance
        if not self.github_instances[self.current_instance_id].exceed_rate_limit:
            return
        # check if there are further instances
        has_further_instances = True
        if self.current_instance_id + 1 == len(self.github_instances):
            # we are already pointing to the last instance
            has_further_instances = False
        if self.github_instances[self.current_instance_id].exceed_rate_limit and has_further_instances:
            print("****** NOTE: We have to change to next instance due to rate limit! ****** ")
            self.current_instance_id += 1
            self.check_instances()
        else:
            raise GitHubCommitServiceException("All GitHub instances have reached their capacity!")
