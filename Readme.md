#COSC 6353 - Software Design
## Identifier Name linter

Author: Suryateja Kurella

PSID : 2050296



> This is a git repository which, when a GIT repository is given  as an input, generates the identifiers to Output1.txt with locations in the format Row, Col


> Also all the identifiers are validated against the rules provided below :

> Capitalisation Anomaly,
>
> Consecutive Underscores
>
> Dictionary Words
>
> Excessive words
>
> Enumeration Identifier Declaration order
>
> External Underscores
>
> Identifier Encoding
>
> Long Identifier Name
>
> Naming Convention Anomaly
>
> Number of words
>
> Numeric Identifier Name
>
> Short Identifier Name
>

# Libraries needed to run this project :

```bash
import sys
import os
import stat
import random
import re
from pathlib import Path
pip install enchant
pip install tree_sitter
pip install GitPython

```

## How to run the code :

Example : python main.py https://github.com/Python-World/python-mini-projects.git .py python Output1.txt Output2.txt


#Output Structure 
## For Output1.txt
identifier = today_day, Row = 8, Col = [4, 13]
```bash
The identifier 'today_day' is in Row 8 and spans from columns 4 to 13
```

## For Output2.txt
identifier = __name__, Row = 24, Col = [3, 11] Failed Reason : ['Naming Convention Anomoly', 'External Underscores', 'Consecutive Underscores']
```bash
The identifier '__name__' is in Row 24 and spans from columns 3 to 11, has the reasons of failures as 'Naming Convention Anomoly', 'External Underscores', 'Consecutive Underscores'
```