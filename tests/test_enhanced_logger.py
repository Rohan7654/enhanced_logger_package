
from enhanced_logger.enhanced_logger import EnhancedLogger

# Test trace logger
trace_logger = EnhancedLogger.configure_trace_logger('trace_logger')

@trace_logger.trace
def sample_function(x, y):
    return x + y

sample_function(5, 10)

# Test performance logger
performance_logger = EnhancedLogger.configure_performance_logger('performance_logger')

@performance_logger.log_performance
def example_function(n):
    total = 0
    for i in range(n):
        total += i
    return total

example_function(1000000)

# Test enhanced performance logger
enhanced_performance_logger = EnhancedLogger.configure_enhanced_performance_logger('enhanced_performance_logger')

@enhanced_performance_logger.log_performance
def compute_factorial(n):
    if n == 0:
        return 1
    else:
        return n * compute_factorial(n - 1)

compute_factorial(10)

# Test JSON logger
json_logger = EnhancedLogger.configure_json_logger('json_logger')
json_logger.info('This is a test log entry in JSON format.')

# Create context information
context_info = {
    'context': {
        'user_id': 12345,
        'transaction_id': 'abcde12345'
    }
}

# Generate log messages with context
json_logger.info('This is a test log entry in JSON format with context.', extra=context_info)

# Test XML logger
xml_logger = EnhancedLogger.configure_xml_logger('xml_logger')
xml_logger.info('This is a test log entry in XML format.')

# Test HTTP logger (Assumes a logging endpoint is available)
# http_logger = EnhancedLogger.configure_http_logger('http_logger', 'http://example.com/log')
# http_logger.info('This is a test log entry sent via HTTP.')

# Test DB logger
db_logger = EnhancedLogger.configure_db_logger('db_logger', 'logs.db')
db_logger.info('This is a test log entry stored in a SQLite database.')

# Test JSON log decorator
@EnhancedLogger.json_log('json_logger')
def add(x, y):
    return x + y

@EnhancedLogger.json_log('json_logger')
def multiply(x, y):
    return x * y

# Test XML log decorator
@EnhancedLogger.xml_log('xml_logger')
def subtract(x, y):
    return x - y

@EnhancedLogger.xml_log('xml_logger')
def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

# Running test functions
print(add(5, 3))
print(multiply(5, 3))
print(subtract(5, 3))
print(divide(5, 3))