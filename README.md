# DynStudio: ALPHA
## A Multi-Platform Intent-Based Automation Module for Python

### Summary:
You can use DynStudio to automate dynamic workflows on multiple platforms. DynStudio use is intent driven, while maintaing good application visibility. As a python module, DynStudio requires knowledge of python programming to properly leverage the automation engine. Through this DynStudio is able to achieve increased workflow flexibility and power. Despite the introduction of Python scripting to intent-based automation, DynStudio aims to still simplify the automation workflow.
The aim of the DynStudio project is to bring the intent-based automation movement into the hands of the python developer, while integrating multi-platform support. DynStudio offers a single pane of glass for automation.

### Introduction:
DynStudio's interface is intent based. This means tasks are outcome oriented (i.e. "Create Object on host"). This is opposition to the task orintation (i.e. "Send command to host"). For example a call to a dynstudio construct may occur thusly;
```
from dynstudio.host import newHost

host = newHost('192.168.0.101','cisco','cisco_ucs')
host.connect('admin', 'Password1')
host.addUser('newAdmin', 'newPassword1')
```

