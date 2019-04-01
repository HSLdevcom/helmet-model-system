# helmet-model-system

## Setup

In "Production-mode" we are using python library dependencies that come with EMME installation.
Add ```%EMMEPATH%\Programs``` to your local PATH-variable to get access to these dependencies.

### Create EMME Bank

- Open EMME Desktop application
- Create new project named 'helmet-model-system' where the path should match your project name & path
  - The wizard should create you a (large binary) file 'helmet-model-system.emp' inside your project folder
- Follow external instructions to configure the EMME-project details.
- End result: Your working folder is filled with EMME-project-specific folders and files and
our [Scripts-folder](Scripts) being one of those folders.

## Running

Run test applications from Scripts folder:

```   
cd Scripts
python assignment_test.py
```   
