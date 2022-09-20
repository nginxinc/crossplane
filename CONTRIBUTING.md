# Contributing Guidelines

Contributions are welcome, and they are greatly appreciated\! Every
little bit helps, and credit will always be given.

## Table of Contents

- [Types of Contributions](#types-of-contributions)
- [Get Started](#get-started)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Tips](#tips)

### Types of Contributions

#### Report Bugs

Report bugs at <https://github.com/nginxinc/crossplane/issues>.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in
troubleshooting.
- Detailed steps to reproduce the bug.

#### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is
open to whoever wants to implement it.

#### Implement Features

Look through the GitHub issues for features. Anything tagged with
"feature" is open to whoever wants to implement it.

#### Write Documentation

crossplane could always use more documentation, whether as part of the
official crossplane docs, in docstrings, or even on the web in blog
posts, articles, and such.

#### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/nginxinc/crossplane/issues>.

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to
implement.
- Remember that this is a volunteer-driven project, and that
contributions are welcome :)

### Get Started

Ready to contribute? Here's how to set up crossplane for local
development.

1. [Fork](https://github.com/nginxinc/crossplane/fork) the crossplane
    repo on GitHub.

2. Clone your fork locally:

        git clone git@github.com:your_name_here/crossplane.git

3. Create a branch for local development:

        git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

4. When you're done making changes, check that your changes pass style
    and unit tests, including testing other Python versions with tox:

        tox

    To get tox, just pip install it.

5. Commit your changes and push your branch to GitHub:

        git add .
        git commit -m "Your detailed description of your changes."
        git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. The pull request should work for CPython 2.7, 3.6, 3.7, 3.8, 3.9, 3.10, and PyPy. Check
    <https://github.com/nginxinc/crossplane/actions/workflows/crossplane-ci.yml> under pull requests for
    active pull requests or run the `tox` command and make sure that the
    tests pass for all supported Python versions.
3. Make sure to add yourself to the Contributors list in AUTHORS.rst :)

### Tips

To run a subset of tests:

    tox -e <env> -- tests/<file>[::test]

To run all the test environments in *parallel* (you need to `pip install
detox`):

    detox
