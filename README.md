# envopt
Wrapper for [docopt](https://github.com/docopt/docopt) to allow ENV variables to override default arguments.


## Usage

Example docopt pydoc:

```python
__doc__ = \
    """ This is an example.

        Usage:
            python my_example.py [options]

        Options:
            -a --a-opt MY_OPT1  # An example option [default: foo]
            -b --b-opt MY_OPT2  # Another example option [default: bar]
            -c --c-opt MY_OPT3  # Yet another example option [default: baz] """
```

Parsing this example without any `ENV` variables set would yield:

```python
from envopt import envopt

print envopt(__doc__)

{ '--a-opt': 'foo',
  '--b-opt': 'bar',
  '--c-opt': 'baz' }
```

However, setting `ENV` variables `A_OPT`, `B_OPT`, or `C_OPT` will override the given defaults:

```python
import os
from envopt import envopt

os.environ['A_OPT'] = 'fe'
os.environ['B_OPT'] = 'fi'
os.environ['C_OPT'] = 'fo'

print envopt(__doc__)

{ '--a-opt': 'fe',
  '--b-opt': 'fi',
  '--c-opt': 'fo' }
```

You can also pass an optional `env_prefix` keyword argument to `envopt` to add a prefix to all the environment variable
names:

```python
import os
from envopt import envopt

os.environ['PROG_A_OPT'] = 'fe'
os.environ['PROG_B_OPT'] = 'fi'
os.environ['PROG_C_OPT'] = 'fo'

print envopt(__doc__, env_prefix='PROG_')

{ '--a-opt': 'fe',
  '--b-opt': 'fi',
  '--c-opt': 'fo' }
```
