
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from re import sub as regExSub

from datetime import datetime

from os import environ as osEnvironment

from github import Github
from github import UnknownObjectException
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from pygh2md.exceptions.InvalidDateFormatException import InvalidDateFormatException
from pygh2md.exceptions.NoGitHubAccessTokenException import NoGitHubAccessTokenException
from pygh2md.exceptions.UnknownGitHubRepositoryException import UnknownGitHubRepositoryException

ENV_GH_TOKEN: str = 'GH_TOKEN'


@dataclass
class GHIssue:
    number:   int = -1
    title:    str = ''
    issueUrl: str = ''


GHIssues = NewType('GHIssues', List[GHIssue])


class GitHubAdapter:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        try:
            gitHubToken: str = osEnvironment[ENV_GH_TOKEN]
        except KeyError:
            raise NoGitHubAccessTokenException

        self._github: Github = Github(gitHubToken)

    def getClosedIssues(self, repositorySlug: str, sinceDate: str) -> GHIssues:
        """

        Args:
            repositorySlug:     In format like 'hasii2001/code-ally-advanced
            sinceDate:          A date string in a format like '2024-02-06'

        Returns: A list of gh issues
        """

        ghIssues: GHIssues = GHIssues([])
        try:
            repo: Repository = self._github.get_repo(repositorySlug)
            self.logger.debug(f'{repo.full_name=}')

            fmt: str  = "%Y-%m-%d"
            datetime_object = datetime.strptime(sinceDate, fmt)
            issues: PaginatedList = repo.get_issues(state='closed', since=datetime_object)
            self.logger.info(f'{issues.totalCount=}')
            for content in issues:
                issue: Issue = cast(Issue, content)

                self.logger.debug(f'{issue=}')

                fixedURL: str = self._fixURL(oldURL=issue.url)

                ghIssue: GHIssue = GHIssue()
                ghIssue.number   = issue.number
                ghIssue.title    = issue.title
                ghIssue.issueUrl = fixedURL

                self.logger.debug(f'{ghIssue=}')

                ghIssues.append(ghIssue)
        except UnknownObjectException:
            raise UnknownGitHubRepositoryException(repositorySlug=repositorySlug)
        except ValueError as e:
            raise InvalidDateFormatException(e)

        return ghIssues

    def _fixURL(self, oldURL: str) -> str:
        """
        Makes the URLs returned by the GitHub API actually user linkable when I
        generate the markdown file.

        e.g.

        https://api.github.com/repos/hasii2011/code-ally-advanced

        gets turned into

        https://github.com//hasii2011/code-ally-advanced

        Args:
            oldURL:  The URL we have to fix

        Returns:  A linkable URL
        """

        apiStrip:  str = regExSub(pattern=r'api.',   repl='', string=oldURL)
        repoStrip: str = regExSub(pattern=r'repos/', repl='', string=apiStrip)

        return repoStrip
