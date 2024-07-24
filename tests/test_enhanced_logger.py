from enhanced_logger import EnhancedLogger

# Test JSON log decorator
@EnhancedLogger.json_log('json_logger', log_to_file='json_logs.log')
def add(x, y):
    return x + y

@EnhancedLogger.json_log('json_logger', log_to_file='json_logs.log')
def multiply(x, y):
    return x * y

# Test Performance Logger
performance_logger = EnhancedLogger.configure_performance_logger('performance_logger', log_to_file='performance_logs.log')

@performance_logger.log_performance
def compute_factorial(n):
    if n == 0:
        return 1
    else:
        return n * compute_factorial(n - 1)

# Test HTTP Logger (Assuming a logging endpoint is available)
http_logger = EnhancedLogger.configure_http_logger('http_logger', 'http://example.com/log', method='POST', headers={'Content-Type': 'application/json'}, log_to_file='http_logs.log')
http_logger.info('This is a test log entry sent via HTTP.')

# Test DB Logger (SQLite)
sqlite_logger = EnhancedLogger.configure_db_logger('sqlite_logger', 'sqlite', {'db_path': 'logs.db'})
sqlite_logger.info('This is a test log entry stored in a SQLite database.')

# Test DB Logger (PostgreSQL)
postgres_logger = EnhancedLogger.configure_db_logger('postgres_logger', 'postgres', {
    'dbname': 'testdb',
    'user': 'dbuser',
    'password': 'dbpass',
    'host': 'localhost',
    'port': 5432
})
# postgres_logger.info('This is a test log entry stored in a PostgreSQL database.')

# Test DB Logger (MongoDB)
mongodb_logger = EnhancedLogger.configure_db_logger('mongodb_logger', 'mongodb', {
    'uri': 'mongodb://localhost:27017/',
    'db_name': 'testdb'
})
mongodb_logger.info('This is a test log entry stored in a MongoDB database.')

# Running test functions
if __name__ == "__main__":
    print(add(5, 3))
    print(multiply(5, 3))
    print(compute_factorial(10))
