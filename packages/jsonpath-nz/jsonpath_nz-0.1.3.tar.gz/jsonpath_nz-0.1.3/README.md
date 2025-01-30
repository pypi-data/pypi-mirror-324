# JSONPath-NZ (NextZen)

A Python library for bidirectional conversion between JSON objects and JSONPath expressions, with support for complex filter conditions and array handling.
- `Author` : Yakub Mohammad (yakub@arusatech.com , arusatechnology@gmail.com) | AR USA LLC

## Features

### Two-way conversion between JSON and JSONPath expressions:
- Convert JSONPath expressions to JSON objects (`parse_jsonpath`)
- Convert JSON objects to JSONPath expressions (`parse_dict`)
- Support for complex filter conditions using `extend` parameter
- Handle nested objects and arrays
- Support array indexing and empty objects
- Maintain data structure integrity

### JSON Pretty Printing
- The package includes a convenient JSON pretty printing utility `jprint` that handles various data formats and provides flexible output options.

#### Parameters

- `data`: The data to print (dict, list, string, or any object)
- `load`: Set to `True` when input is a JSON string that needs parsing
- `marshall`: Set to `True` to convert non-JSON-serializable objects to strings
- `indent`: Number of spaces for indentation (default: 2)

### Enhanced Python Logger
- A flexible basic logging utility `log` that uses Python's built-in logging functionality with additional features like file capture and detailed tracebacks.
- Console and file logging support
- Capture specific log messages to file
- Detailed traceback information
- Consistent formatting across console and file outputs
- File name and line number tracking
- Dynamic log file configuration (example : `log.config(log_file_name)`)

#### Log Levels
- `log.debug(msg)` - Detailed information for debugging
- `log.info(msg)` - General information about program execution
- `log.warning(msg)` - Warning messages for potentially problematic situations
- `log.error(msg)` - Error messages for serious problems
- `log.critical(msg)` - Critical messages for fatal errors
- `log.traceback(e)` - Detailed exception information can be used in try/except blocks

## Installation

```bash
pip install jsonpath-nz
```

## Usage

### Converting JSONPath to Dictionary (`parse_jsonpath(<Dict of JSONPath>,extend=<extend filter dictionary>)`)
### Converting Dictionary to JSONPath (`parse_dict(<Dictionary>,extend=<extend filter dictionary>)`)

- See the [tests/test_parse_jsonpath.py and tests/test_parse_dict.py] files for examples.

- Define extend parameter for filter conditions

# JSONPath Extend Filter given as parameter 

The extend filter in JSONPath allows complex filtering of arrays based on multiple conditions. It uses the syntax:

[?(@.field1 == 'value1' && @.field2 == 'value2')]

Example:
`$.loanApplication.borrower[?(@.firstName == 'John' && @.lastName == 'wright')].contact`

This filters array elements where:
- firstName equals 'John' AND
- lastName equals 'wright'

Key features:
- Uses @ to reference current element
- Supports multiple conditions with && (AND)
- Can access nested properties
- Returns matching elements only

## API Reference

### parse_jsonpath(manifest, extend=None)

Converts JSONPath expressions to a dictionary structure.

Parameters:
- `manifest` (dict): Dictionary with JSONPath expressions as keys and values
- `extend` (dict, optional): Dictionary specifying filter conditions for arrays

Returns:
- dict: Processed dictionary structure

Example:

```python
from jsonpath_nz import parse_jsonpath, jprint
JSONPath expressions
jsonpath_data = {
    "$.store.book[1].author": "Yakub Mohammad",
    "$.store.local": "False",
    "$.channel": "online",
    "$.loanApplication.borrower[?(@.firstName == 'John' && @.lastName == 'Doe')].contact": "9876543210",
    "$.loanApplication.borrower[?(@.firstName == 'John' && @.lastName == 'wright')].contact": "9876543211"
}
extend = {
    "borrower": ["firstName", "lastName"]
}
result = parse_jsonpath(jsonpath_data, extend=extend)
jprint(result)
```
Output:
```
{
  "store": {
    "book": [
      {},
      {
        "author": "Yakub Mohammad"
      }
    ],
    "local": "False"
  },
  "channel": "online",
  "loanApplication": {
    "borrower": [
      {
        "firstName": "(John)",
        "lastName": "(Doe)",
        "contact": "9876543210"
      },
      {
        "firstName": "(John)",
        "lastName": "(wright)",
        "contact": "9876543211"
      }
    ]
  }
}
```

### parse_dict(data, parent_path='$', paths=None, extend=None)

Converts a dictionary to JSONPath expressions.

Parameters:
- `data` (dict): Input dictionary to convert
- `parent_path` (str, optional): Base JSONPath. Defaults to '$'
- `paths` (dict, optional): Dictionary to store results
- `extend` (dict, optional): Dictionary specifying filter fields for arrays

Returns:
- dict: Dictionary with JSONPath expressions as keys and values

Example:

```python
from jsonpath_nz import parse_dict, jprint

# Dictionary to convert
dict_data = {
    "store": {"book": [{"author": "Yakub Mohammad"}, {"category": "Fiction"}]},
    "channel": "online",
    "loanApplication": {'borrower': [
        {'firstName': 'John', 'lastName': 'Doe', 'contact': '9876543210'},
        {'firstName': 'John', 'lastName': 'wright', 'contact': '9876543211'}]}
}

extend = {
    "borrower": ["firstName", "lastName"]
}

result = parse_dict(dict_data, extend=None)
jprint(result)
```

Output:
```bash
{
  "$.store.book[1].author": "Yakub Mohammad",
  "$.store.local": "False",
  "$.channel": "online",
  "$.loanApplication.borrower[?(@.firstName == 'John' && @.lastName == 'Doe')].contact": "9876543210",
  "$.loanApplication.borrower[?(@.firstName == 'John' && @.lastName == 'wright')].contact": "9876543211"
}
```

## Error Handling

Both functions include error handling for:
- Invalid JSONPath syntax
- Unbalanced brackets or quotes
- Missing required fields
- Invalid filter conditions

## JSON Pretty Printing

- In the above example of parse_jsonpath and parse_dict functions, the output is printed using the `jprint` function.

## Logging

- The `log` function is used to log messages to the console and file.
- See the [tests/test_log.py] file for examples.

Example:

```python
from jsonpath_nz import log
log.config("app.log") # this is optional(default log capture to <temp directory>/arlog_<timestamp>.log)
log.info("This is a test message")
log.error("This is an error message")
log.critical("This is a critical message", capture=True) # this will capture to file
log.warning("This is a warning message" , 1) # this will capture to file
log.debug("This is a debug message")
def test_traceback():   
    try:
        #divide by zero
        a = 1/0
        raise Exception("This is a test exception")
    except Exception as e:
        log.traceback(e)
        log.error("This is an trace back message--",1)
test_traceback()
```

Output:
```
2025-01-05 00:21:31,881 - INFO      [test_log.py:12] This is a test message
2025-01-05 00:21:31,881 - ERROR     [test_log.py:13] This is an error message
2025-01-05 00:21:31,881 - CRITICAL  [test_log.py:14] This is a critical message
2025-01-05 00:21:31,882 - WARNING   [test_log.py:15] This is a warning message
2025-01-05 00:21:31,882 - DEBUG     [test_log.py:16] This is a debug message
2025-01-05 00:21:31,883 - ERROR     [test_log.py:25] ======= TRACEBACK =======
TRACEBACK: << test_traceback >> [C:\Users\arusa\tools\GIT\jsonpath-nz\tests\test_log.py:22]
ZERODIVISIONERROR: division by zero
2025-01-05 00:21:31,883 - ERROR     [test_log.py:26] This is an trace back message--
```










