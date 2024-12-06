# Introduction 
Common code for Data Science Projects 

# Getting Started
Use as a submodule of other repos

This snippet seems handy for importing packages from GeneralStore in Python by just their name

```python
import os
import sys
module_path = os.path.abspath(os.path.join('../GeneralStore'))
if module_path not in sys.path:
    sys.path.append(module_path)
```
assuming a folder structure like

```
-repo
--GeneralStore
---package
--models
---file.py or ipynb

```

# Build and Test


# Contribute
