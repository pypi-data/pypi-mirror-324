
from typing import cast

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from click import ClickException
from click import command
from click import option
from click import version_option

from click import echo as clickEcho

from pygh2md import __version__ as gh2mdVersion

from pygh2md.GitHubAdapter import GHIssue
from pygh2md.GitHubAdapter import GHIssues
from pygh2md.GitHubAdapter import GitHubAdapter
from pygh2md.GitHubAdapter import ENV_GH_TOKEN

from pygh2md.exceptions.InvalidDateFormatException import InvalidDateFormatException
from pygh2md.exceptions.NoGitHubAccessTokenException import NoGitHubAccessTokenException
from pygh2md.exceptions.UnknownGitHubRepositoryException import UnknownGitHubRepositoryException


NON_BREAKING_SPACE: str = '&nbsp;'


class PyGh2Md:
    def __init__(self, outputFileName: str):

        self.logger: Logger = getLogger(__name__)

        self._outputFileName: str = outputFileName

    def convert(self, repoSlug: str, sinceDate: str, append: bool = True):

        gitHubAdapter: GitHubAdapter = GitHubAdapter()

        ghIssues: GHIssues = gitHubAdapter.getClosedIssues(repositorySlug=repoSlug, sinceDate=sinceDate)
        clickEcho(f'Retrieved issue count: {len(ghIssues)}')

        mode: str = 'a'
        if append is False:
            mode = 'w'

        with open(self._outputFileName, mode) as outputFile:
            outputFile.write(f'{repoSlug}{osLineSep}')
            outputFile.write(f'---------------------{osLineSep}{NON_BREAKING_SPACE}')
            outputFile.write(f'{osLineSep}')

            for issue in ghIssues:
                ghIssue: GHIssue = cast(GHIssue, issue)

                mdLine: str = (
                    f'* [{ghIssue.number}]({ghIssue.issueUrl}) {ghIssue.title} {osLineSep}'
                )
                outputFile.write(mdLine)
            outputFile.write(f'---------------------{osLineSep}')


@command()
@version_option(version=f'{gh2mdVersion}', message='%(version)s')
@option('-s', '--slug',        required=True,                              help='GitHub slugs to query')
@option('-d', '--since-date',  required=True,                              help='The date from which we want to start searching.')
@option('-o', '--output-file', required=True,                              help='The output markdown file.')
@option('-a', '--append',      required=False, is_flag=True, default=True, help='Append to output file')
def pygh2md(slug: str, since_date: str, output_file: str, append: bool = True):
    """

    slug            A repository slug in the format <user-name>/repository-name; e.g., `hasii2011/TestRepository`

    sinceDate       The start date to query for closed issues; Format yyyy-mm-dd; e.g., 2024-03-01

    output_file     The filename for the markdown output file

    appends If `True` append this script's output (default is True)

    """
    try:
        gh2md: PyGh2Md = PyGh2Md(outputFileName=output_file)

        gh2md.convert(repoSlug=slug, sinceDate=since_date, append=append)

    except NoGitHubAccessTokenException:
        raise ClickException(f'No GitHub token specified in `{ENV_GH_TOKEN}`')
    except InvalidDateFormatException:
        raise ClickException('The input date format is not valid. ex: 2024-03-01')
    except UnknownGitHubRepositoryException:
        raise ClickException(f'Unknown GitHub Repository: {slug}')


if __name__ == "__main__":

    pygh2md(['-s', 'hasii2011/code-ally-advanced', '-d', '2024-02-01', '-o', 'codeallyadvanced.md'])
    # pygh2md(['--help'])
    # pygh2md(['-s', 'hasii2011/code-ally-advanced', '-d', '204-02-01', '-o', 'codeallyadvanced.md'])
