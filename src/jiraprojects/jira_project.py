class JiraProject:

    def __init__(self, name, prefix, num_issues, comments):
        self.name = name
        """ :type : str """
        self.prefix = prefix
        """ :type : str """
        self.num_issues = num_issues
        """ :type : int """
        self.comments = comments
        """ :type : dict{issue_key: num_comments} """

    def metrics(self):
        """
        Calculates all comment metrics for a project:

        - total lines of comments
        - average lines of comments per issue
        - issues with comments
        - average comments per commented issues
        - min #comments for an issue
        - max #comments for an issue
        - percentage of issues without comments

        :return: Metrics for A Jira Project
        :rtype: dict()

        :Example:

        >>> metrics()
        {
            "total": 75345,
            "average": 4.5,
            "commented_issues": 45987,
            "average_commented": 6.3,
            "min": 0,
            "max": 34,
            "percentage_without": 0.12
        }
        """
        total = issues_with_comments = max = without = 0
        min = 100
        for issue_key, num_comments in self.comments.items():
            total += num_comments
            if num_comments > 0:
                issues_with_comments += 1
            if num_comments < min:
                min = num_comments
            if num_comments > max:
                max = num_comments
            if num_comments == 0:
                without += 1
        return {
            "total": total,
            "average": total / self.num_issues,
            "commented_issues": issues_with_comments,
            "average_commented": total / issues_with_comments,
            "min": min,
            "max": max,
            "percentage_without": without / self.num_issues
        }
