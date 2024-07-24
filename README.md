# Enhanced Logger
--------------------------
[![PyPI version](https://badge.fury.io/py/enhanced_logger.svg)](https://pypi.org/project/enhanced-logger/)
[![Downloads](https://pepy.tech/badge/enhanced_logger)](https://pypi.org/project/enhanced-logger/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

The `Enhanced Logger` package is an extension of the built-in Python `logging` module, designed to address additional features and performance metrics. This package includes:

- Trace logging to log all function entry and exit
- JSON and XML formatters
- Performance metrics logging
- HTTP and database logging handlers
- File logging for all logger types (except DB Handler)

## Features

- **Trace Logging:** Log entry and exit points of functions with context.
- **Performance Metrics:** Log execution time and memory usage of functions.
- **Enhanced Formatters:** Log entries in JSON and XML formats.
- **HTTP Logging:** Send log entries to a remote server via HTTP.
- **Database Logging:** Store log entries in various types of databases (SQLite, PostgreSQL, MongoDB).
- **File Logging:** Option to store logs in a `.log` file.

## Installation

To install the Enhanced Logger package, use the following command:

```sh
pip install enhanced-logger
```

## Usage

### Trace Logger

Trace logging allows you to trace the entry and exit points of functions.

```python
from enhanced_logger import EnhancedLogger

trace_logger = EnhancedLogger.configure_trace_logger('trace_logger')

@trace_logger.trace
def sample_function(x, y):
    return x + y

sample_function(5, 10)

```

### Performance Logger

Performance logging provides execution time and memory usage information.

```python
from enhanced_logger import EnhancedLogger

performance_logger = EnhancedLogger.configure_performance_logger('performance_logger')

@performance_logger.log_performance
def example_function(n):
    total = 0
    for i in range(n):
        total += i
    return total

example_function(1000000)

```

### Enhanced Performance Logger

Enhanced performance logging with additional details.

```python
from enhanced_logger import EnhancedLogger

enhanced_performance_logger = EnhancedLogger.configure_enhanced_performance_logger('enhanced_performance_logger')

@enhanced_performance_logger.log_performance
def compute_factorial(n):
    if n == 0:
        return 1
    else:
        return n * compute_factorial(n - 1)

compute_factorial(10)

```
### JSON Formatter

Logs entries in JSON format.

```python
from enhanced_logger import EnhancedLogger

json_logger = EnhancedLogger.configure_json_logger('json_logger')
json_logger.info('This is a test log entry in JSON format.')

```
You can also log context data.
```python
from enhanced_logger import EnhancedLogger

json_logger = EnhancedLogger.configure_json_logger('json_logger')
context_info = {
    'context': {
        'user_id': 12345,
        'transaction_id': 'abcde12345'
    }
}
json_logger.info('This is a test log entry in JSON format with context.', extra=context_info)

```
or you can also use decorator.
```python
@EnhancedLogger.json_log('json_logger')
def add(x, y):
    return x + y

@EnhancedLogger.json_log('json_logger')
def multiply(x, y):
    return x * y

print(add(5, 3))
print(multiply(5, 3))

```

### XML Formatter

Logs entries in XML format.

```python
from enhanced_logger import EnhancedLogger

xml_logger = EnhancedLogger.configure_xml_logger('xml_logger')
xml_logger.info('This is a test log entry in XML format.')

```

### HTTP Handler

Sends log entries to a remote server via HTTP. (Assumes a logging endpoint is available)

```python
from enhanced_logger import EnhancedLogger

http_logger = EnhancedLogger.configure_http_logger('http_logger', 'http://example.com/log', method='POST', headers={'Content-Type': 'application/json'})
http_logger.info('This is a test log entry sent via HTTP.')

```

### DB Handler

Stores log entries in various types of databases likes SQLite/Postgres/MongoDB.

#### SQLite
```python
from enhanced_logger import EnhancedLogger

sqlite_logger = EnhancedLogger.configure_db_logger('sqlite_logger', 'sqlite', {'db_path': 'logs.db'})
sqlite_logger.info('This is a test log entry stored in a SQLite database.')

```

#### PostgreSQL
```python
from enhanced_logger import EnhancedLogger
postgres_logger = EnhancedLogger.configure_db_logger('postgres_logger', 'postgres', {
    'dbname': 'testdb',
    'user': 'dbuser',
    'password': 'dbpass',
    'host': 'localhost',
    'port': 5432
})
postgres_logger.info('This is a test log entry stored in a PostgreSQL database.')

```
#### MongoDB
```python
from enhanced_logger import EnhancedLogger
mongodb_logger = EnhancedLogger.configure_db_logger('mongodb_logger', 'mongodb', {
    'uri': 'mongodb://localhost:27017/',
    'db_name': 'testdb'
})
mongodb_logger.info('This is a test log entry stored in a MongoDB database.')

```
### More Examples
You can also store logs in a `.log` file by specifying file name for the `log_to_file` argument.

```python
from enhanced_logger import EnhancedLogger

# JSON Logger
@EnhancedLogger.json_log('json_logger', log_to_file='json_logs.log')
def add(x, y):
    return x + y

print(add(5, 3))


# Performance Logger
performance_logger = EnhancedLogger.configure_performance_logger('performance_logger', log_to_file='performance_logs.log')

@performance_logger.log_performance
def compute_factorial(n):
    if n == 0:
        return 1
    else:
        return n * compute_factorial(n - 1)

print(compute_factorial(10))

# HTTP Logger
from enhanced_logger import EnhancedLogger

http_logger = EnhancedLogger.configure_http_logger('http_logger', 'http://example.com/log', method='POST', headers={'Content-Type': 'application/json'}, log_to_file='http_logs.log')
http_logger.info('This is a test log entry sent via HTTP.')

```