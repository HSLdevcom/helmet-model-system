[![Build Status](https://travis-ci.org/HSLdevcom/helmet-model-system.svg?branch=master)](https://travis-ci.org/HSLdevcom/helmet-model-system)

# helmet-model-system

This repository contains python files for Helmet 4.0 Model System. Source codes can be found in the [Scripts-folder](Scripts).

## Usage

In this chapter, we will guide you how to install HELMET 4.0 to work with INRO Emme software. The user is not expected to install any new software apart from [helmet-model-system](https://github.com/HSLdevcom/helmet-model-system) and [helmet-ui](https://github.com/HSLdevcom/helmet-ui).

If you do not have an Emme license or you wish to develop HELMET 4.0 further, please scroll down to [Development](#development) chapter.

### Setup

In production, we are using Python 2.7 which is supported by and installed together with INRO Emme software.

We are using those Python dependencies that come with INRO Emme installation. To get access to these dependencies, you need to add them to your local PATH variable:

1. Open Control Panel.
2. Go to User Accounts, then click again User Accounts, then select from the left hand menu "Change my environment variables".
3. From the top box ("User variables for USERNAME"), find and select "Path" variable, and click "Edit...".
4. Click "New" and write `%EMMEPATH%\Programs`.
5. Click OK in the "Edit enrivonment variable" window, and then click OK again in the "Environment Variables" window.

Next, you need to initialize an Emme project:

1. Open Emme desktop application.
2. Create new project called `helmet-model-system` in which the path should match your project name and path.
   - The wizard should create you a (large binary) file called `helmet-model-system.emp` inside your project folder
3. Follow external instructions to configure the details of the Emme project. Now, your working folder is filled with Emme project specific folders and files.
4. From this repository, copy the contents of the [Scripts](Scripts) folder to the "Scripts" folder in the Emme project.

### Running

You can run HELMET 4.0 from the command line or by using [helmet-ui](https://github.com/HSLdevcom/helmet-ui). Before running from the command line, set the configurations in [dev-config.json](Scripts/dev-config.json). Then, open command line to your Emme project and type:

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
