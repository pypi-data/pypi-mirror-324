#!/usr/bin/env python
"""
dsbuild – A multi-purpose build and packaging helper for Python projects.

This script provides commands for:
  * Building Python wheel packages.
  * Cleaning build artifacts.
  * Running tests with coverage.
  * Generating version files.
  * Managing namespace- vs. non-namespace-based libraries.

It relies on a local virtual environment (unless DSBUILD_ALLOW_NON_VENV is set),
and offers additional options such as checking for newer dsbuild releases on PyPI.
Run `dsbuild --help` or `dsbuild <subcommand> --help` for usage details.
"""

import glob
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from argparse import Action, ArgumentParser, Namespace, RawTextHelpFormatter
from configparser import ConfigParser, NoSectionError
from inspect import signature
from setuptools import find_namespace_packages, find_packages
from typing import Any, cast

from packaging.version import parse

# Local Folder
from . import __version__
from .version import get_version

# path to the directories
_VENV_NAME = '.venv'
_WHEELS_DIR_NAME = 'wheels'
_BUILD_DIR_NAME = 'build'
_VENV_BIN_SEARCH_DIRS = ['Scripts', 'bin']

##################################################

PYTHON_PREFIX_DIR = sys.prefix

# This script can only be executed from a suitable virtual environment.
if not os.path.basename(PYTHON_PREFIX_DIR) == _VENV_NAME:
    # The following is a workaround for the fact that:
    #       - dsbuild still contains the versioning logic; and
    #       - when doing editable installs of a dependency in the context of docker
    #         image creation, there is no venv, but only system Python.
    # To deal with this problem, an environment variable DSBUILD_ALLOW_NON_VENV allows
    # continuing also when this script is not run from inside a venv. This is a
    # temporary measure (and as such is not announced in the changelog) and will
    # disappear as soon as versioning logic is split off from dsbuild.
    if not os.environ.get('DSBUILD_ALLOW_NON_VENV', False):
        raise RuntimeError('Running from a non-virtual environment is unsupported.')
    else:
        import warnings

        warnings.warn(
            'Running outside of a virtual environment because the environment variable '
            '`DSBUILD_ALLOW_NON_VENV=1`. Continuing without any guarantees!!',
            stacklevel=1,
        )


def check_for_a_new_version(package_name: str, package_version: str):
    """
    Check if there is a newer version of the package on PyPI.

    The function grabs the list of all the versions of the package from PyPI filtering
    out the pre-releases and checks if the last version is greater than the specified
    one.

    It works best if all the versions are PEP440 compatible. Otherwise the rules for
    filtering and comparison can be found here:
    - https://packaging.pypa.io/en/latest/version.html

    Args:
        package_name: a name of the package to check.
        package_version: the version of the package to compare to PyPI.
    """
    # Get list of all versions from PyPI
    try:
        pypi_index_url = f'https://pypi.python.org/pypi/{package_name}/json'
        pypi_index = json.load(urllib.request.urlopen(pypi_index_url))
        available_versions = [parse(v) for v in pypi_index['releases']]
        available_versions = [v for v in available_versions if not v.is_prerelease]
    except Exception:
        print(f'Warning: unable to check for a new version of {package_name}')
        return

    if not available_versions:
        return

    latest_version = available_versions[-1]
    current_version = parse(package_version)

    if latest_version > current_version:
        print(
            f'Warning: {package_name} {latest_version} is available, while you are '
            f'still using {current_version}. Please consider updating.'
        )
        if latest_version.major > current_version.major:
            print(
                'Warning: There may be breaking changes compared to the version '
                'you are using. Please review the release notes carefully.'
            )
        else:
            print(
                'Note: There are no breaking changes in a new version compared to '
                'the one you are using, only new features and bugfixes - the update '
                'should be safe!'
            )


def get_venv_dir() -> str:
    """Get the full path to the directory that is supposed to contain the local venv."""
    return PYTHON_PREFIX_DIR


def get_project_root_dir() -> str:
    """
    Get the root directory for this project or package.

    This dir is determined using the assumption that the venv dir is created at this
    top-level.

    Returns:
        A path to the root directory of the project.
    """
    return os.path.realpath(os.path.join(get_venv_dir(), '..'))


def get_venv_executable(executable: str, required: bool = True) -> str | None:
    """
    Return the full path to an executable inside a given virtual environment.

    Args:
        executable: Name of the executable.
        required: Whether to consider it a fatal error if the executable is not found.

    Returns:
        Full path to an executable inside the virtual environment. In case it cannot be
            found, either an exception is raised or None is returned, depending on
            whether the executable is required or not.

    Raises:
        FileNotFoundError: When the executable is required and could not be found.
    """
    search_path = [os.path.join(get_venv_dir(), p) for p in _VENV_BIN_SEARCH_DIRS]
    venv_executable = shutil.which(executable, path=os.pathsep.join(search_path))

    if required and not venv_executable:
        raise FileNotFoundError(
            f'The virtual environment executable could not be '
            f'found: {executable} in {search_path}'
        )

    return venv_executable


def get_venv_python(required: bool = True) -> str | None:
    """
    Return the Python executable inside a given virtual environment.

    Args:
        required (bool): Whether to consider it a fatal error if the executable is not
            found.

    Returns:
        Full path to the Python executable inside the virtual environment. In case it
            cannot be found, either an exception is raised or None is returned,
            depending on whether the executable is required or not.

    Raises:
        FileNotFoundError: When the executable is required and could not be found.
    """
    return get_venv_executable(
        executable=os.path.basename(sys.executable), required=required
    )


def get_lib_version(changelog_path: str | None = None) -> str:
    """Wrapper around version.get_lib_version to provide a sensible default argument."""
    if changelog_path is None:
        changelog_path = os.path.join(get_project_root_dir(), 'Changelog.md')

    return get_version(changelog_path=changelog_path)


##################################################
# Helpers to define the sub commands of this script.


def format_parser_description(subparsers: Action) -> str:
    """
    Format the list of subparsers with their descriptions for the console.

    Formatting is done by aligning the "<subparser name>: <subparser description>" lines
    by a ":" symbol to achieve the following effect:

            short_name: description for the short name
                  name: description for the name
        very_long_name: description for the very long name

    Args:
        subparsers: a name of the package to check.

    Returns:
        A formatted string (containing newline symbols) with the subparser names and
            descriptions.
    """
    subparsers_description = {k: v.description for k, v in subparsers.choices.items()}
    max_command_length = len(max(subparsers_description, key=len))

    formatted_descriptions = [
        f'{k:>{max_command_length}}: {v}' for k, v in subparsers_description.items()
    ]
    return '\n'.join(formatted_descriptions)


def call_command(arguments: Namespace) -> Any:
    """
    Calls a function stored in `command_function` argument.

    It requires the argument to contain a callable object under a `command_function`
    argument as well as the arguments for all the function parameters.

    This implementation is inspired by the trick described in the documentation of the
    argparse subparsers functionality:
    https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers

    Arguments:
        arguments: an argparse namespace with the parsed arguments.

    Returns:
        The result of the function call.

    Raises:
        RuntimeError: When the function call cannot be performed due to missing
            arguments.
    """
    command_function = arguments.command_function

    command_parameters = signature(command_function).parameters.keys()
    arguments_dict = vars(arguments)

    missing_arguments = set(command_parameters) - set(arguments_dict)

    if missing_arguments:
        raise RuntimeError(
            'The following arguments are missing for a function call to '
            f'{command_function}: {list(missing_arguments)}'
        )

    kwargs = {k: arguments_dict[k] for k in command_parameters}

    return command_function(**kwargs)


def read_dsbuild_config(config_path: str | None = None) -> dict[str, str | bool]:
    """
    Reads the config file that contains a dsbuild section.

    If the file does not exist, the default config is returned, which
    would look like this in the configuration file:

    [dsbuild]
    package_prefix =
    test_dir = lib/tests
    check_for_a_new_version = True
    namespace_package_topdirs = ["lib"]
    """
    # default config
    dsbuild_conf: dict[str, str | bool] = {
        'package_prefix': '',
        'namespace_package_topdirs': '["lib"]',
        'test_dir': 'lib/tests',
        'check_for_a_new_version': True,
    }

    # default config path
    if config_path is None:
        config_path = os.path.join(get_project_root_dir(), 'setup.cfg')

    # try to read the configuration file
    try:
        config = ConfigParser()
        config.read(config_path)
        dsbuild_conf.update(dict(config.items('dsbuild')))
    except FileNotFoundError:
        # if the file does not exist, we just return defaults
        pass
    except NoSectionError:
        # if the [dsbuild] section does not exist, we just return defaults
        pass

    # Ensure boolean values
    for k in ['check_for_a_new_version']:
        dsbuild_conf[k] = dsbuild_conf[k] in [True, 'True', 'true', 'Yes', 'yes']

    # load json serialized values
    for k in ['namespace_package_topdirs']:
        dsbuild_conf[k] = json.loads(cast(str, dsbuild_conf[k]))

    return dsbuild_conf


def find_library(folder: str) -> tuple[str, bool]:
    """
    Locate a Python library and identify if it's normal or part of a namespace package.

    Args:
        folder: the folder containing the setup.py file

    Returns:
        str, bool: path to library, False if normal library, True if namespace package
    """
    # try to find a normal library first
    try:
        package = find_packages(folder)
        package = [p for p in package if '.' not in p]
        if len(package) > 1:
            raise ValueError(
                'dsbuild supports only repos with a single library or'
                'multiple namespace packages.'
            )
        return os.path.join(folder, package[0]), False
    except IndexError:
        pass

    # try to find a namespace package
    try:
        package = find_namespace_packages(folder)
        package = [p for p in package if '.' not in p]
        package = package[0]
        is_namespace_pkg = True
    except IndexError:
        raise FileNotFoundError('No library could be found in:', folder)
    return os.path.join(folder, package), is_namespace_pkg


def get_library_dirs(toplevel_dirs_to_check: list[str]) -> list[str]:
    """
    Get the paths to the Python library-containing folders.

    A folder contains a library if it contains a `setup.py` file. There are two
    options:
    1. Simple library: A single `setup.py` file is present in the top-level.
    2. Namespace packages: Possibly multiple `setup.py` files can be found
                           underneath the `./lib` directory.

    Args:
        toplevel_dirs_to_check: List of folders (subfolders of project_root_dir) where
            Python library-containing folders will be searched.

    Returns:
        a list of folders that contain the python library (the folder containing the
            setup.py file)
    """
    project_root_dir = get_project_root_dir()

    # Option 1: Simple library, `setup.py` in top-level.
    if os.path.exists(os.path.join(project_root_dir, 'setup.py')):
        return [project_root_dir]

    # Option 2: Namespace packages.
    setup_files = []
    for toplevel in toplevel_dirs_to_check:
        setup_files += glob.glob(
            os.path.join(project_root_dir, toplevel, '**', 'setup.py'), recursive=True
        )

    return [os.path.dirname(f) for f in setup_files]


def cmd_help():
    subprocess.check_call([sys.executable, __file__, '--help'])


def cmd_clean():
    """Clean the root directory of the project to ensure a clean build."""
    dirs_to_clean = [_WHEELS_DIR_NAME, _BUILD_DIR_NAME, 'docs/build']

    project_root_dir = get_project_root_dir()
    for dirname in dirs_to_clean:
        path = os.path.abspath(os.path.join(project_root_dir, dirname))
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
        except OSError as e:
            raise OSError(
                f"The folder '{path}' could not be deleted, "
                'so we are not sure that all build files are fresh.'
            ) from e
        print(f"Cleaned directory '{path}'.")


def cmd_wheel():
    """Build a wheel of the library."""
    project_root_dir = get_project_root_dir()
    wheels_dir = os.path.abspath(os.path.join(project_root_dir, _WHEELS_DIR_NAME))
    dsbuild_config = read_dsbuild_config()

    libraries = get_library_dirs(dsbuild_config['namespace_package_topdirs'])
    if not libraries:
        raise ValueError(f'No python libraries could be found in {project_root_dir}')

    for library in libraries:
        lib_folder, is_namespace_pkg = find_library(library)

        if is_namespace_pkg:
            lib_name = os.path.basename(library)
        else:
            lib_name = os.path.basename(lib_folder)

        package_name = dsbuild_config['package_prefix'] + lib_name
        this_wheel_dir = os.path.join(wheels_dir, package_name)

        # run the wheel creation command
        command = [
            get_venv_python(),
            '-m',
            'build',
            '--wheel',
            '--outdir',
            this_wheel_dir,
        ]
        subprocess.check_call(command, cwd=library)

    print(f"Wheel(s) created in '{wheels_dir}'")


def cmd_test():
    """
    Run unittests and coverage report.

    The tests are being picked up from a directory with name matching the pattern
    `*_test` or from `lib/tests`. Note that at most a single directory on disk should
    match. If not, this is considered a fatal error. Also, note that independently of
    which directory contained the tests, the output directly will always be
    `lib/tests_results`.
    """
    project_root_dir = get_project_root_dir()
    dsbuild_config = read_dsbuild_config()

    # check if we can find libraries, otherwise raise exception
    libs = get_library_dirs(dsbuild_config['namespace_package_topdirs'])
    if not libs:
        raise ValueError(f'No python libraries could be found in {project_root_dir}')

    # Get a list of (existing) folders that can contain tests.
    test_folders = []
    # 1. Legacy: dirs of the form `*_test`
    test_folders += [
        f
        for f in glob.glob(os.path.join(project_root_dir, '*_test'))
        if os.path.isdir(f)
    ]
    # 2. Custom (or new): By default `lib/tests`, but can be configured in `setup.cfg`.
    test_dir = os.path.join(project_root_dir, dsbuild_config['test_dir'])
    test_folders += [f for f in [test_dir] if os.path.isdir(test_dir)]

    if len(test_folders) == 0:
        print('Could not find a folder with unittests. No tests will be run.')
        return

    if len(test_folders) > 1:
        raise FileNotFoundError(
            f'Could not find a unique folder with unittests. Found: {test_folders}.'
        )

    test_folder = test_folders[0]

    # Define the output dir.
    test_output_dir = os.path.join(project_root_dir, 'lib', 'tests_results')

    # We only want to report coverage info for the source files in our library (i.e. we
    # need to provide a suitable filter to `--cov=...` when running pytest).
    # For this purpose we use the library directories found in the project. Each of them
    # needs to have its own '--cov' argument.
    cov_args = [f'--cov={os.path.relpath(lib, project_root_dir)}' for lib in libs]

    # run tests
    command = [
        get_venv_python(),
        '-m',
        'pytest',
        test_folder,
        f'--junitxml={test_output_dir}/test-results.xml',
        *cov_args,
        '--cov-branch',
        '--cov-report=term',
        f'--cov-report=xml:{test_output_dir}/coverage.xml',
        f'--cov-report=html:{test_output_dir}/html',
    ]
    subprocess.check_call(command, cwd=project_root_dir)

    print(f'Ran all unittests. Output is written to: {test_output_dir}.')


def cmd_version(changelog: str):
    """
    Print library version.

    Args:
        changelog: An optional path to the changelog.
    """
    lib_version = get_lib_version(changelog_path=changelog)
    print(lib_version)


def cmd_generate_version_py():
    """Generate a self-sufficient version.py script."""
    src = os.path.join(os.path.dirname(__file__), 'version.py')
    dst = os.path.join(get_project_root_dir(), 'version.py')

    with open(src, 'r') as fin, open(dst, 'w') as fout:
        header = (
            f'#########################################################################'
            f'###############\n'
            f'#\n'
            f'# THIS FILE WAS AUTO-GENERATED BY DSBUILD {__version__}.\n'
            f'#\n'
            f'# IT SHOULD BE COMMITTED TO THE PROJECT ROOT DIRECTORY AND PREFERABLY '
            f'NOT MODIFIED\n'
            f'# MANUALLY.\n'
            f'#\n'
            f'# YOU CAN ALWAYS REGENERATE IT BY RUNNING:\n'
            f'#   $ dsbuild generate-version-py\n'
            f'#\n'
            f'#########################################################################'
            f'###############\n\n\n'
        )

        fout.write(header)
        fout.write(fin.read())

    print(f'Version.py file generated at {dst}')


def cmd_all():
    """Convenience mode that does 'everything' from scratch (build, test, packaging)."""
    cmd_clean()
    cmd_test()
    cmd_wheel()


def cmd_package():
    """Convenience mode that does a clean packaging."""
    cmd_clean()
    cmd_wheel()


def main():
    """Main entry point for the dsbuild script."""
    parser = ArgumentParser(
        prog='dsbuild',
        formatter_class=RawTextHelpFormatter,
        description=(),
    )
    parser.add_argument(
        '--version', '-v', action='version', version=f'%(prog)s {__version__}'
    )

    subparsers = parser.add_subparsers()

    sp = subparsers.add_parser(
        'clean', description='Clean the project root directory to ensure a clean build.'
    )
    sp.set_defaults(command_function=cmd_clean)

    sp = subparsers.add_parser('wheel', description='Build wheel.')
    sp.set_defaults(command_function=cmd_wheel)

    sp = subparsers.add_parser('test', description='Run unittests + coverage.')
    sp.set_defaults(command_function=cmd_test)

    sp = subparsers.add_parser(
        'version', description='Determine the version of a library.'
    )
    sp.add_argument(
        '--changelog',
        '-clog',
        default=None,
        help='Path to the Changelog.md file for version parsing.',
    )
    sp.set_defaults(command_function=cmd_version)

    sp = subparsers.add_parser(
        'generate-version-py',
        description='Generate a self-sufficient version.py at the project root.',
    )
    sp.set_defaults(command_function=cmd_generate_version_py)

    sp = subparsers.add_parser('all', description='clean + test + docs + wheel.')
    sp.set_defaults(command_function=cmd_all)

    sp = subparsers.add_parser('package', description='clean + docs + wheel.')
    sp.set_defaults(command_function=cmd_package)

    parser.description = (
        f'This script helps to build and package python libraries.\n'
        f'{format_parser_description(subparsers)}'
    )

    args = parser.parse_args()

    dsbuild_config = read_dsbuild_config()

    if dsbuild_config['check_for_a_new_version']:
        check_for_a_new_version('dsbuild', __version__)

    call_command(args)


if __name__ == '__main__':
    main()
