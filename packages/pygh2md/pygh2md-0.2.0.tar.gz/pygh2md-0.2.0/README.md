
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/hasii2011/pygh2md/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/hasii2011/pygh2md/tree/master)
[![PyPI version](https://badge.fury.io/py/pygh2md.svg)](https://badge.fury.io/py/pygh2md)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Introduction

A simple python console script to let me convert [GitHub Closed Issues](https://docs.github.com/en/github-cli) output to [Markdown](https://www.howtogeek.com/448323/what-is-markdown-and-how-do-you-use-it/).

Typically after working a multi-repository project I want to know the issues in each repository that have been fixed since the last release. 

It produces output in the following format:

```markdown
* [121](https://api.github.com/repos/hasii2011/pytrek/issues/121) Implement Move automatic 
* [120](https://api.github.com/repos/hasii2011/pytrek/issues/120) Fixing of devices is not asynchronous 
* [119](https://api.github.com/repos/hasii2011/pytrek/issues/119) We should only have a single Super Commander 
```

# Overview

The basic command structure is:

```
Usage: pygh2md [OPTIONS]

  slug            A repository slug in the format <user-name>/repository-name;
  e.g., `hasii2011/TestRepository`

  sinceDate       The start date to query for closed issues; Format yyyy-mm-
  dd; e.g., 2024-03-01

  output_file     The filename for the markdown output file

  appends If `True` append this script's output (default is True)

Options:
  --version               Show the version and exit.
  -s, --slug TEXT         GitHub slugs to query  [required]
  -d, --since-date TEXT   The date from which we want to start searching.
                          [required]
  -o, --output-file TEXT  The output markdown file.  [required]
  -a, --append            Append to output file
  --help                  Show this message and exit.
```


A simple example:

```bash
pygh2md -s hasii2011/pytrek -d 2024-06-01 -o PytrekClosedIssues.md
```

# Installation

```bash
pip install pygh2md
```

___

Written by Humberto A. Sanchez II <mailto@humberto.a.sanchez.ii@gmail.com>, (C) 2024


## Note
For all kind of problems, requests, enhancements, bug reports, etc.,
please drop me an e-mail.


------


![Humberto's Modified Logo](https://raw.githubusercontent.com/wiki/hasii2011/gittodoistclone/images/SillyGitHub.png)

I am concerned about GitHub's Copilot project



I urge you to read about the
[Give up GitHub](https://GiveUpGitHub.org) campaign from
[the Software Freedom Conservancy](https://sfconservancy.org).

While I do not advocate for all the issues listed there I do not like that
a company like Microsoft may profit from open source projects.

I continue to use GitHub because it offers the services I need for free.  But, I continue
to monitor their terms of service.

Any use of this project's code by GitHub Copilot, past or present, is done
without my permission.  I do not consent to GitHub's use of this project's
code in Copilot.
