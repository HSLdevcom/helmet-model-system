# OMX 

Emme supports OpenMatrix library for exporting matrices. 

- More info here: https://github.com/osPlanning/omx/wiki/EMME 
- Python source codes: https://github.com/osPlanning/omx-python
- Useful tool for exporting from cmd line: https://github.com/bstabler/EMXtoOMX

## Known issues

Released EMME contains version 0.2 of OMX which is exported via module OMX. However if we want to install OMX via PyPi it is released using the name OpenMatrix (because of name clash with another library). This causes us problems when importing the library, f.ex:

```   
import omx # Installed via EMME 
import openmatrix as omx # Installed via PyPi, the "correct" way. see https://github.com/osPlanning/omx-python#installation
```   

OMX and other libraries are installed to EMME application folder into <EMME_installation_folder>\python-lib\win64\2.7\vendor\omx

As a fix we could just download the released 0.2 version from here: https://github.com/osPlanning/omx/releases/tag/v0.2 and import OMX as static dependency to all envs. 
