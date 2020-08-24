[![Build Status](https://travis-ci.com/HSLdevcom/helmet-model-system.svg?branch=master)](https://travis-ci.com/HSLdevcom/helmet-model-system)

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
5. Click OK in the "Edit environment variable" window, and then click OK again in the "Environment Variables" window.

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

If you do not have INRO Emme license or you wish to develop HELMET 4.0 source code, you need to set up a development environment. Although not covered here, installing [Git](https://git-scm.com/downloads) is highly recommended!

### Environment and dependencies

We are using Python 2.7 because it is supported by INRO Emme software.

1. Install Python 2.7. (2020-04-16: Do not install Python 2.7.17 because it will not work correctly until [this issue](https://github.com/pypa/pipenv/issues/4016) is resolved. Install Python 2.7.16 instead.)
2. Add `C:\Python27` and `C:\Python27\Scripts` to your local PATH variable in "Environment Variables".
3. Open a new Command Prompt and type `python --version`. You should get `Python 2.7.16` or some other Python 2.7 version. 

`pip` is the recommended package installer for Python. The normal Python installation routine installs `pip` to `C:\Python27\Scripts`. Type `pip --version` to Command Prompt to check if `pip` is installed and in your PATH. The command should return `pip 20.0.2 from c:\python27\lib\site-packages\pip (python 2.7)` (`pip` version may vary).

We are using `pipenv` to import the same open source libraries which INRO Emme software uses. `pipenv` isolates our environment from the other global Python modules and makes sure we don't break anything with our setup. Optional introduction to `pipenv` can be found from [Python docs](https://docs.python-guide.org/dev/virtualenvs/) or [Jonathan Cutrer's blog](https://jcutrer.com/python/pipenv-pipfile).

1. Open Command Prompt.
2. Install `pipenv` by running `python -m pip install --user pipenv`. `pipenv` should now be installed in `%APPDATA%\Python\Scripts` (e.g. `C:\Users\USERNAME\AppData\Roaming\Python\Scripts`).
3. Add `%APPDATA%\Python\Scripts` to your local PATH variable.
4. Close and reopen Command Prompt and check that `pipenv` is recognised by typing `pipenv --version`. It should return `pipenv, version 2018.11.26`.
4. Download [helmet-model-system](https://github.com/HSLdevcom/helmet-model-system) repository and open a Command Prompt to its "Scripts" folder.
5. Install dependencies from `Pipfile`:
    - First setup: `pipenv --python 2.7 install --dev`
    - Additional syncing if new packages are added: `pipenv --python 2.7 sync --dev`
6. Depending on your operating system, rename either `.env-win` (Windows) or `.env-nix` (Linux) to `.env`. In Windows, you can do this in Command Propmpt by typing `copy .env-win .env`.

Now, you should have a virtual environment in `C:\Users\USERNAME\.virtualenvs\Scripts-xxxxxxxx\Lib\site-packages`.

Use `pipenv` when executing scripts. For example:

```
cd Scripts
pipenv run python test_assignment.py
```

### Visual Studio Code

The following extensions are recommended when developing with Visual Studio Code:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Test Explorer UI](https://marketplace.visualstudio.com/items?itemName=hbenl.vscode-test-explorer)
- [Python Test Explorer for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter)

A couple of tips to get it all working:

- Remember to first setup your development environment. After that, open "Scripts" folder in Visual Studio Code, and select your virtual environment from bottom left Python interpreter list.
- To configure tests, click `Ctrl-Shift-P`, type `Python: Configure tests`, select `pytest` framework, and `tests` as the directory containing tests. Tests should appear in the Test Explorer (click the chemistry bottle from the left).

### OMX 

Emme supports OpenMatrix library for exporting matrices. 

- More info here: https://github.com/osPlanning/omx/wiki/EMME 
- Python source codes: https://github.com/osPlanning/omx-python
- Useful tool for exporting from cmd line: https://github.com/bstabler/EMXtoOMX
