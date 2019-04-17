# helmet-model-system

This repository contains python files for Helmet 4.0 Model System. Source codes can be found in the [Scripts-folder](Scripts).

## Setup

We have two execution environments:
- deployed "production" environment
- local development environment

In both cases we're using Python version 2.7 because our final deployment target (EMME) supports only 2.7.
Also the final prodution version is always run on Windows because EMME only supports windows.

*Deployed production env*

In "Production-mode" we are using python library dependencies that come with EMME installation.
Add ```%EMMEPATH%\Programs``` to your local PATH-variable to get access to these dependencies.
At the moment user is not expected to install any software, other than the provided scripts in the [Scripts-folder](Scripts).

*Local development env*

In the development setup we're using *pipenv* to isolate our environment from the other python modules.
intro to pipenv can be found from these links:
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
pipenv --python 2.7 install
# Once setup is done you can just run
pipenv --python 2.7 sync
```

Install new libraries when needed (will update Pipfile, please commit that to repository):

```   
pipenv --python 2.7 install <your-new-library>
```


### Create EMME Bank

- Open EMME Desktop application
- Create new project named 'helmet-model-system' where the path should match your project name & path
  - The wizard should create you a (large binary) file 'helmet-model-system.emp' inside your project folder
- Follow external instructions to configure the EMME-project details.
- End result: Your working folder is filled with EMME-project-specific folders and files and
our [Scripts-folder](Scripts) being one of those folders.


## Tests

We're using PyTest framework. Test are in [tests-folder](Scripts/tests) and can be invoked with

```   
pipenv run pytest
```


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

The dependencies included in this repository are licensed under their own terms.

- Numpy: https://www.numpy.org/license.html
- PyTables: https://github.com/PyTables/PyTables/blob/master/LICENSE.txt
- OpenMatrix: https://github.com/osPlanning/omx-python/blob/master/LICENSE.TXT
