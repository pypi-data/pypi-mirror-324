#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright (c) 2024 - 2025 -- Lars Heuer
#
"""\
Nox test runner configuration.
"""
import os
import sys
import re
from functools import partial
from itertools import chain
import shutil
import nox

_PY_VERSIONS = ('3.10', '3.11', '3.12', '3.13')
_PY_DEFAULT_VERSION = sys.version[:4]

nox.options.sessions = [f'test-{_PY_DEFAULT_VERSION}']

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=_PY_VERSIONS)
def test(session):
    """\
    Run test suite.
    """
    session.install('-Ur', 'tests/requirements.txt')
    session.install('.')
    session.run('py.test')


@nox.session(python=_PY_DEFAULT_VERSION)
def docs(session):
    """\
    Build the documentation.
    """
    session.install('-Ur', 'docs/requirements.txt')
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), 'output'))
    shutil.rmtree(output_dir, ignore_errors=True)
    doctrees, html, man = map(partial(os.path.join, output_dir), ['doctrees', 'html', 'man'])
    session.install('.')
    session.cd('docs')
    sphinx_build = partial(session.run, 'sphinx-build', '-W', '-d', doctrees, '.')
    sphinx_build('-b', 'html', html)
    sphinx_build('-b', 'man', man)
    sys.path.insert(0, os.path.abspath('..'))
    import gabbia
    if 'dev' not in gabbia.__version__:
        shutil.copyfile(os.path.join(man, 'gabbia.1'),
                        os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'data/usr/share/man/man1/', 'gabbia.1')))
        session.log("'man/gabbia.1' has been modified, don't forget to commit")

@nox.session(python=_PY_DEFAULT_VERSION)
def lint(session):
    """\
    Run linters.
    """
    session.install('.')
    session.install('ruff', 'mypy')
    session.run('mypy', 'gabbia.py')
    session.run('ruff', 'check', '--show-fixes', '.')


#
# Release related tasks
# 1. nox -e start-release -- version-number
# 2. run tests, update docs, update changes
# 3. nox -e finish-release -- version-number
# 4. git push / git push origin --tags
# 5. nox -e build-release -- version-number
# 6. nox -e upload-release
#


@nox.session(name='start-release', python=_PY_DEFAULT_VERSION)
def start_release(session):
    """\
    Prepares a release.

    * Creates a new branch release-VERSION_NUMBER
    * Changes the version number in gabbia.__version__ to VERSION_NUMBER
    * Sets gabbia._DEBUG to False
    """
    session.install('packaging')
    git = partial(session.run, 'git', external=True)
    git('checkout', 'main')
    prev_version = _get_current_version(session)
    version = _validate_version(session)
    valid_version = bool(int(session.run('python', '-c', 'from packaging.version import parse;'
                                                         f'prev_version = parse("{prev_version}");'
                                                         f'next_version = parse("{version}");'
                                                         'print(1 if prev_version < next_version else 0)',
                                         silent=True)))
    if not valid_version:
        session.error('Invalid version')
    release_branch = f'release-{version}'
    git('checkout', '-b', release_branch, 'main')
    _change_debug_status(session)
    session.install('.')
    gabbia_debug = bool(int(session.run('python', '-c', 'import gabbia; print(int(gabbia._DEBUG))', silent=True)))
    if gabbia_debug:
        session.error('gabbia._DEBUG is not False')
    _change_version(session, prev_version, version)
    git('add', 'gabbia.py')
    session.log(f'Now on branch "{release_branch}". Run the tests, run nox -e docs. Update and add CHANGES')
    session.log('Commit any changes.')
    session.log(f'When done, call nox -e finish-release -- {version}')


@nox.session(name='finish-release', python=_PY_DEFAULT_VERSION)
def finish_release(session):
    """\
    Finishes the release.

    * Merges the branch release-VERSION_NUMBER into master
    * Creates a tag VERSION_NUMBER
    * Increments the development version
    """
    version = _validate_version(session)
    release_branch = f'release-{version}'
    git = partial(session.run, 'git', external=True)
    git('checkout', 'main')
    git('merge', '--no-ff', release_branch, '-m', f'Merge release branch {release_branch}')
    git('tag', '-a', version, '-m', f'Release {version}')
    git('branch', '-d', release_branch)
    version_parts = version.split('.')
    patch = str(int(version_parts[2]) + 1)
    next_version = '.'.join(chain(version_parts[:2], patch)) + '.dev0'
    _change_version(session, version, next_version)
    _change_debug_status(session)
    git('add', 'gabbia.py')
    git('commit', '-m', 'Incremented development version')
    session.log('Finished. Run git push / git push origin --tags and '
                f'nox -e build-release -- {version} / nox -e upload-release')


@nox.session(name='build-release', python=_PY_DEFAULT_VERSION)
def build_release(session):
    """\
    Builds a release: Creates sdist and wheel
    """
    version = _validate_version(session)
    session.install('build', 'wheel')
    git = partial(session.run, 'git', external=True)
    git('fetch')
    git('fetch', '--tags')
    git('checkout', version)
    shutil.rmtree('dist', ignore_errors=True)
    session.run('python', '-m', 'build', '--no-isolation')
    git('checkout', 'master')


@nox.session(name='upload-release', python=_PY_DEFAULT_VERSION)
def upload_release(session):
    """\
    Uploads a release to PyPI
    """
    session.install('twine')
    twine = partial(session.run, 'twine')
    twine('check', 'dist/*')
    twine('upload', 'dist/*')


def _validate_version(session):
    if not session.posargs:
        session.error('No release version provided')
    elif len(session.posargs) > 1:
        session.error('Too many arguments')
    version = session.posargs[0]
    if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+$', version):
        session.error(f'Invalid version number: "{version}"')
    return version


def _get_current_version(session):
    """\
    Returns the current version as string.
    """
    fn = os.path.abspath(os.path.join(os.path.dirname(__file__), 'gabbia.py'))
    with open(fn, encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'^__version__: Final = ["\']([^"\']+)["\']$', content, flags=re.MULTILINE)
    if m:
        return m.group(1)
    session.error('Cannot find any version information')


def _change_version(session, previous_version, next_version):
    """\
    Changes the __version__ from previous_version to next_version.
    """
    fn = os.path.abspath(os.path.join(os.path.dirname(__file__), 'gabbia.py'))
    with open(fn, encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(fr'^(__version__: Final = ["\'])({re.escape(previous_version)})(["\'])$',
                         fr'\g<1>{next_version}\g<3>', content, flags=re.MULTILINE)
    if content != new_content:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return
    session.error(f'Cannot modify version. Provided: "{previous_version}" (previous) "{next_version}" (next)')


def _change_debug_status(session):
    """\
    Changes _DEBUG constant from True to False and vice versa.
    """
    fn = os.path.abspath(os.path.join(os.path.dirname(__file__), 'gabbia.py'))
    with open(fn, encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(r'^_DEBUG: Final = (\w+)$',
                         lambda m: f'_DEBUG: Final = {m.group(1) != "True"}',
                         content, 1, flags=re.MULTILINE)
    if content != new_content:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return

