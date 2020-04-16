[![Build Status](https://travis-ci.org/HSLdevcom/helmet-model-system.svg?branch=master)](https://travis-ci.org/HSLdevcom/helmet-model-system)

# helmet-model-system

This repository contains python files for Helmet 4.0 Model System. Source codes can be found in the [Scripts-folder](Scripts).

## Usage

### Setup

*Deployed production env: EMME*

In "Production-mode" we are using python library dependencies that come with EMME installation.
Add ```%EMMEPATH%\Programs``` to your local PATH-variable to get access to these dependencies.
At the moment user is not expected to install any software, other than the provided scripts in the [Scripts-folder](Scripts).

*For Production setup: Create EMME Bank

- Open EMME Desktop application
- Create new project named 'helmet-model-system' where the path should match your project name & path
  - The wizard should create you a (large binary) file 'helmet-model-system.emp' inside your project folder
- Follow external instructions to configure the EMME-project details.
- End result: Your working folder is filled with EMME-project-specific folders and files and
our [Scripts-folder](Scripts) being one of those folders.

### Running

In deployed-mode (with EMME) run application from command line or using [Helmet UI](https://github.com/HSLdevcom/helmet-ui). Before running from command line, configurations in [dev-config.json](Scripts/dev-config.json) need to be set.

```
cd Scripts
python helmet.py
```

Emme assignment can be tested without further configuration:

```
cd Scripts
python test_assignment.py
```

## Development

### Environment

We have two execution environments:
- deployed "production" environment
- local development environment

In both cases we're using Python version 2.7 because our final deployment target (EMME) supports only 2.7.

### Dependencies

*Local development env: Pipenv*

In the development setup we're using *pipenv* to import the libraries. Pipenv isolates our environment from the other global python modules and makes sure we don't break anything else with our setup.   

Intro to pipenv can be found from these links:
- https://docs.python-guide.org/dev/virtualenvs/
- https://jcutrer.com/python/pipenv-pipfile

1) Pre-requirement is to have some Python2 version and pip installed. Recommendation is to install
pip to user home (%APPDATA%/Python/Scripts/pip.exe) and keep it out of the system PATH.
You can use [import-python helper script](Scripts/import-python.bat) in case you installed it to the local user.

2) Install pipenv (unless you already have it).   

```
pip install --user pipenv
```

3) Then install the requirements from Pipfile using pipenv.  

```
# First setup:
pipenv --python 2.7 install --dev
# Once setup is done you can just run
pipenv --python 2.7 sync --dev
```

Install new libraries when needed (will update Pipfile, please commit that to repository):

```
pipenv --python 2.7 install <your-new-library>
```

### Tests

We're using PyTest framework. Test are in [tests-folder](Scripts/tests) and can be invoked with

```
pipenv run pytest tests
```

Remember to give the folder as parameter, otherwise pytest will run all the tests with the dependencies also. Also, remember to run `Scripts/import-dev-dependencies.bat` to get the path to Python libraries in `Scripts/pythonlibs`.

In case you wish to run tests on Visual Studio Code, do either of the following:

1. Rename `Scripts/.env-win` as `Scripts/.env`, or
2. Open workspace settings by pressing Ctrl + Shift + P and selecting "Preferences: Open Workspace Settings", and add the line `"python.envFile": "${workspaceFolder}/.env-win"`.

Now Visual Studio Code should discover all tests.

### Running

During development when using pipenv:

```
cd Scripts
pipenv run python test_assignment.py
```
