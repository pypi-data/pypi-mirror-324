# common-py

My common Python hacks

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation
To install the required dependencies, use:
```bash
pip install ekcommon  
```
To use: 
```
from commonpy import * 
```

## Usage

### Example 1: Handling Exceptions
```python
from commonpy.simpleexceptioncontext import SimpleExceptionContext

callback = lambda e: self._eng.statusChanges.emit(f'Exception in processing {e}')
with SimpleExceptionContext('exception in processing',callback=callback):
    ret=self.process_internal(ls)
    logging.debug(f"process end {ret}")
    return ret

```
In this example , a callback is called when the exception occurs. 


### Example 2: Exception Handling with Decorators
```python

@simple_exception_handling(err_description='error in get_symbol_history', return_succ=(None, []), never_throw=True)
@excp_handler(polygon.exceptions.BadResponse, handler=excphandler)
def get_symbol_history(sym, startdate, enddate, iscrypto=False):
    # Your code to fetch symbol history here
    pass 
```
### Example 3: Date and Time Utilities

```python
from commonpy import localize_it, unlocalize_it
import datetime

dt = datetime.datetime.now()
localized_dt = localize_it(dt)
unlocalized_dt = unlocalize_it(localized_dt)
```
## Features
- **SimpleExceptionContext**: Context manager for handling exceptions with customizable logging and traceback formatting.
- **Date and Time Utilities**: Functions to localize and unlocalize datetime objects.
- **Functional Helpers**: Various lambda functions for filtering dictionaries and mapping lists.

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request.

## License
This project is licensed under the MIT License.
