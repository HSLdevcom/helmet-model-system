[![Build Status](https://travis-ci.org/HSLdevcom/helmet-model-system.svg?branch=master)](https://travis-ci.org/HSLdevcom/helmet-model-system)


# helmet-model-system

This repository contains python files for Helmet 4.0 Model System. Source codes can be found in the [Scripts-folder](Scripts).

## Setup

We have two execution environments:
- deployed "production" environment
- local development environment

In both cases we're using Python version 2.7 because our final deployment target (EMME) supports only 2.7.
Also the final prodution version is always run on Windows because EMME only supports windows.

### Dependencies

We have several external dependencies in our codebase, f.ex NumPy and OMX, etc. Reason for including them to this repository is because the version of the OMX-library used by EMME is highly custom and cannot be found from normal PyPi repositories.

Importing the dependencies depend on the environment (local-development or production). In production-mode they come via EMME and in development we use PipEnv.


*Deployed production env: EMME*

In "Production-mode" we are using python library dependencies that come with EMME installation.
Add ```%EMMEPATH%\Programs``` to your local PATH-variable to get access to these dependencies.
At the moment user is not expected to install any software, other than the provided scripts in the [Scripts-folder](Scripts).


*Local development env: Pipenv*

In the development setup we're using two approaches to import the libraries:

- part of the libraries are included as static depencies and are located in [./Scripts/pythonlibs/ folder](./Scripts/pythonlibs/). This is because they don't install very nicely from PyPi-public repositories.
  - When developing locally you need to import the libraries to PYTHONPATH.
    - This can happen either by using the script [import-dev-dependencies.bat](./Scripts/import-dev-dependencies.bat)
	- OR by using pipenv, which then loads the PYTHONPATH via the [.env file](./Scripts/.env)
- Other more compatible libraries are installed via *pipenv*. Pipenv isolates our environment from the other global python modules and makes sure we don't break anything else with our setup.   

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


### For Production setup: Create EMME Bank

- Open EMME Desktop application
- Create new project named 'helmet-model-system' where the path should match your project name & path
  - The wizard should create you a (large binary) file 'helmet-model-system.emp' inside your project folder
- Follow external instructions to configure the EMME-project details.
- End result: Your working folder is filled with EMME-project-specific folders and files and
our [Scripts-folder](Scripts) being one of those folders.


## Tests

We're using PyTest framework. Test are in [tests-folder](Scripts/tests) and can be invoked with

```   
pipenv run pytest tests
```

Remember to give the folder as parameter, otherwise pytest will run all the tests with the dependencies also. Also, remember to run `Scripts/import-dev-dependencies.bat` to get the path to Python libraries in `Scripts/pythonlibs`.

In case you wish to run tests on Visual Studio Code, do either of the following:

1. Rename `Scripts/.env-win` as `Scripts/.env`, or
2. Open workspace settings by pressing Ctrl + Shift + P and selecting "Preferences: Open Workspace Settings", and add the line `"python.envFile": "${workspaceFolder}/.env-win"`.

Now Visual Studio Code should discover all tests.

## Running

In deployed-mode (with EMME) run test applications from Scripts folder:

```   
cd Scripts
python assignment_test.py
```   

During development when using pipenv:

```   
cd Scripts
pipenv run python assignment_test.py
```   

## Licenses

The dependencies included in this repository are licensed under their own terms:

- Numpy: https://www.numpy.org/license.html
- PyTables: https://github.com/PyTables/PyTables/blob/master/LICENSE.txt
- OpenMatrix: https://github.com/osPlanning/omx-python/blob/master/LICENSE.TXT
